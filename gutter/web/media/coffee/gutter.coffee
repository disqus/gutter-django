swtch =
  disabled: '1'
  selective: '2'
  global: '3'

ensure_correct_visibility_for = (row) ->
  $conditions = $(row).find('section.conditions')
  $select = $(row).find('select[name=state]')

  switch $select.val()
    when swtch.disabled, swtch.global then $conditions.hide()
    when swtch.selective then $conditions.show()

ensure_correct_arguments_for = (row) ->
  # Remove existing inputs from the row
  row.find('input[type=text]').remove()

  $operator = row.find('select[name$="operator"]')

  name_prefix = $operator.attr('name').split('-')[0..2].join('-')
  new_arguments = $operator.find('option:selected').data('arguments').split(',')

  $.each new_arguments, (index, argument) ->
    input = $('<input>').attr(name: name_prefix + '-' + argument, type: 'text')
    row.append(input)


attr_setter = (attr_name, number) ->
  (index, element) ->
    name_parts = $(element).attr(attr_name).split('-')
    name_parts[1] = number + 1
    $(element).attr(attr_name, name_parts.join('-'))

add_condition_to = (row) ->
  prototype = $(row).find('ul.conditions li:last-child').first()
  clone = prototype.clone(true, true)

  prototype.parent('ul.conditions').append(clone)
  clone.find('input,select').removeAttr('selected').attr('value', '')

  recalculate_condition_attrs_for(row)

remove_condition = (condition) ->
  row = $(condition).parents('ul.switches li')
  $(condition).remove()
  recalculate_condition_attrs_for(row)

recalculate_condition_attrs_for = (row) ->
  condition_rows = $(row).find('ul.conditions li').each (index, element) ->
    $(element).find('input,select').map(attr_setter('name', index))
    $(element).find('input,select').map(attr_setter('id', index))
    $(element).find('label').map(attr_setter('for', index))

$ ->

  $state_selects = $('ul.switches li select[name=state]')

  $state_selects.change (event) ->
    row = $(this).parents('li')
    ensure_correct_visibility_for(row)

  $('select[name$="operator"]').change (event) ->
    row = $(this).parent('li')
    ensure_correct_arguments_for(row)

  $('ul.switches li section.conditions button[data-action=add]').click (event) ->
    event.preventDefault()
    row = $(event.currentTarget).parents('li')[0]
    add_condition_to(row)

  $('ul.switches li section.conditions button[data-action=remove]').click (event) ->
    event.preventDefault()
    condition = $(event.currentTarget).parents('li')[0]
    remove_condition(condition)

  # Setup things for the first time
  $.map($('ul.switches li'), ensure_correct_visibility_for)