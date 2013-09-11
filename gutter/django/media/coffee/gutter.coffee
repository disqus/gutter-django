swtch =
  disabled: '1'
  selective: '2'
  global: '3'

update_conditions_visibility = (event) ->
  $conditions = $(this).parents('ul.switches li').find('section.conditions')

  switch $(this).val()
    when swtch.disabled, swtch.global then $conditions.hide()
    when swtch.selective then $conditions.show()

remove_operator_arguments = (event) ->
  $(event.target).siblings('input[type=text]').remove()

add_operator_arguments = (event) ->
  $operator = $(event.target)

  name_prefix = $operator.attr('name').split('-')[0..1].join('-')
  new_arguments = $operator.find('option:selected').data('arguments').split(',')

  $.each new_arguments, (index, argument) ->
    new_attrs =
      name: name_prefix + '-' + argument
      type: 'text'
      id: 'id_' + name_prefix + '-' + argument
      class: 'added'

    input = $('<input>').attr(new_attrs)
    label = $('<label>').attr(for: new_attrs.id).text(argument)

    $operator.parent('section.condition').append(label).append(input)

add_condition = (event) ->
  $conditions = $(this).parents('.switch_form').find('ul.conditions')
  $prototype = $('ul#condition-form-prototype li').first()
  $prototype.clone(true, true).appendTo($conditions)

  $conditions.find('li').last().find('input,select').removeAttr('selected').attr('value', '')

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
      name_parts[1] = number
      $(element).attr(attr_name, name_parts.join('-'))


  condition_rows = $(this).find('ul.conditions li').each (index, element) ->
    $(element).find('input,select').map(attr_setter('name', index))
    $(element).find('input,select').map(attr_setter('id', index))
    $(element).find('label').map(attr_setter('for', index))


recalculate_total_forms = (event) ->
  count = $(this).find('ul.conditions li').length
  $(this).find('input[name$=TOTAL_FORMS]').val(count)
  false


adjust_submit_visibility = (event) ->
  inputs_and_selects = $(this).find('ul.conditions').find('input,select')

  if inputs_and_selects.not('[value]').length > 0
    $(this).find('input[type=submit]').attr(disabled: true)
  else
    $(this).find('input[type=submit]').attr(disabled: false)

  false

$ ->

  $('.switch_form').delegate('select[name=state]', 'change', update_conditions_visibility)
  $('.switch_form').delegate('select[name$=operator]', 'change', remove_operator_arguments)
  $('.switch_form').delegate('select[name$=operator]', 'change', add_operator_arguments)
  $('.switch_form').delegate('button[data-action=add]', 'click', add_condition)
  $('.switch_form').delegate('button[data-action=remove]', 'click', remove_condition)

  $('.switch_form').on('gutter.switch.conditions.changed', recalculate_condition_attrs)
  $('.switch_form').on('gutter.switch.conditions.changed', recalculate_total_forms)
  $('.switch_form').on('gutter.switch.conditions.changed', adjust_submit_visibility)

  $('.switch_form').delegate 'input,select', 'blur change keypress', ->
    $(this).trigger('gutter.switch.conditions.changed')

  $('button.addSwitch').click ->
    new_switch = $('#switch-__new__').show()
    inputs = new_switch.find('ul.conditions').find('input,select')
    inputs.removeAttr('selected').attr('value', '')
    new_switch.trigger('gutter.switch.conditions.changed')
    false

  # Setup delete button
  $('ul.switches').find('input[name=delete]').hide()
  $('ul.switches').find('label[for=id_delete]').hide()

  $('<button data-action="delete">Delete Switch</button>').appendTo('form section.actions')
  $('button[data-action=delete]').click ->
    $(this).parents('form').find('input[name=delete]').attr(checked: 'checked')

  $('#switch-__new__').hide()
  $('.switch_form select[name=state]').trigger('change')
