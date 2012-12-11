swtch =
  disabled: '1'
  selective: '2'
  global: '3'

update_conditions_visibility = (event) ->
  $conditions = $(this).parents('ul.switches li').find('section.conditions')
  console.log($conditions.length)

  switch $(this).val()
    when swtch.disabled, swtch.global then $conditions.hide()
    when swtch.selective then $conditions.show()

remove_operator_arguments = (event) ->
  $(event.target).siblings('input[type=text]').remove()

add_operator_arguments = (event) ->
  $operator = $(event.target)

  name_prefix = $operator.attr('name').split('-')[0..2].join('-')
  new_arguments = $operator.find('option:selected').data('arguments').split(',')

  $.each new_arguments, (index, argument) ->
    input = $('<input>').attr(name: name_prefix + '-' + argument, type: 'text')
    $operator.parent('section.condition').append(input)

add_condition = (event) ->
  $conditions = $(this).parents('ul.switches').find('ul.conditions')

  prototype = $conditions.find('li').first()
  clone = prototype.clone(true, true)

  clone.appendTo($conditions)
  clone.find('input,select').removeAttr('selected').attr('value', '')
  $(this).trigger('gutter.switch.conditions.changed')

  false


remove_condition = (event) ->
  $conditions = $(this).parents('ul.conditions')

  $(this).parents('ul.conditions li').remove()
  $conditions.trigger('gutter.switch.conditions.changed')
  false

recalculate_condition_attrs = (event) ->
  attr_setter = (attr_name, number) ->
    (index, element) ->
      name_parts = $(element).attr(attr_name).split('-')
      name_parts[1] = number + 1
      $(element).attr(attr_name, name_parts.join('-'))


  condition_rows = $(this).find('ul.conditions li').each (index, element) ->
    $(element).find('input,select').map(attr_setter('name', index))
    $(element).find('input,select').map(attr_setter('id', index))
    $(element).find('label').map(attr_setter('for', index))


$ ->

  $('ul.switches li').delegate('select[name=state]', 'change', update_conditions_visibility)
  $('ul.switches li').delegate('select[name$=operator]', 'change', remove_operator_arguments)
  $('ul.switches li').delegate('select[name$=operator]', 'change', add_operator_arguments)
  $('ul.switches li').delegate('button[data-action=add]', 'click', add_condition)
  $('ul.switches li').delegate('button[data-action=remove]', 'click', remove_condition)
  $('ul.switches li').live('gutter.switch.conditions.changed', recalculate_condition_attrs)

  $('ul.switches li select[name=state]').trigger('change')
