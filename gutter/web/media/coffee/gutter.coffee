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

add_condition_to = (row) ->
  event.preventDefault()

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
    row = $(event.currentTarget).parent('li')[0]
    add_condition_to(row)

  # Setup things for the first time
  $.map($('ul.switches li'), ensure_correct_visibility_for)