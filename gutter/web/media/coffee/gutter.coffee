swtch =
  disabled: '1'
  selective: '2'
  global: '3'

ensure_correct_visibility_for = (selects) ->
  conditions = $(selects).parents('li').find('ul.conditions')

  switch $(selects).val()
    when swtch.disabled, swtch.global then conditions.hide()
    when swtch.selective then conditions.show()

handle_operator_for = (operator) ->
  $operator = $(operator)
  $parent = $(operator).parent('li')

  existing = $parent.find('input[type=text]').remove()

  name_prefix = $operator.attr('name').split('-')[0..2].join('-')
  new_arguments = $operator.find('option:selected').data('arguments').split(',')

  $.each new_arguments, (index, argument) ->
    input = $('<input>').attr(name: name_prefix + '-' + argument, type: 'text')
    $operator.parent('li').append(input)

$ ->
  # Changes to elements
  $('ul.switches li select[name=state]').change -> ensure_correct_visibility_for(this)
  $('select[name$="operator"]').change -> handle_operator_for(this)

  # Setup things for the first time
  all_state_selects = $('ul.switches li select[name=state]')
  ensure_correct_visibility_for(all_state_selects)