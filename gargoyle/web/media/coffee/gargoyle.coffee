swtch =
  disabled: '1'
  selective: '2'
  global: '3'

ensure_correct_visibility_for = (selects) ->
  conditions = $(selects).parents('li').find('div..conditions')

  switch $(selects).val()
    when swtch.disabled, swtch.global then conditions.hide()
    when swtch.selective then conditions.show()

handle_operator_for = (operator) ->
  arguments = $(operator).find('option:selected').data('arguments').split(',')
  $.each(arguments) (index, argument) ->
    input = $('input').attr('name', '')

$ ->

  all_state_selects = $('ul.switches li select[name="switch[state]"]')

  # Changes to elements
  $('ul.switches li select').change -> ensure_correct_visibility_for(this)
  $('select.operator').change -> handle_operator_for(this)

  # Setup things for the first time
  ensure_correct_visibility_for(all_state_selects)