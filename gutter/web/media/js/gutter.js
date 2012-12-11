(function() {
  var ensure_correct_visibility_for, handle_operator_for, swtch;

  swtch = {
    disabled: '1',
    selective: '2',
    global: '3'
  };

  ensure_correct_visibility_for = function(selects) {
    var conditions;
    conditions = $(selects).parents('li').find('ul.conditions');
    switch ($(selects).val()) {
      case swtch.disabled:
      case swtch.global:
        return conditions.hide();
      case swtch.selective:
        return conditions.show();
    }
  };

  handle_operator_for = function(operator) {
    var $operator, $parent, existing, name_prefix, new_arguments;
    $operator = $(operator);
    $parent = $(operator).parent('li');
    existing = $parent.find('input[type=text]').remove();
    name_prefix = $operator.attr('name').split('-').slice(0, 3).join('-');
    new_arguments = $operator.find('option:selected').data('arguments').split(',');
    return $.each(new_arguments, function(index, argument) {
      var input;
      input = $('<input>').attr({
        name: name_prefix + '-' + argument,
        type: 'text'
      });
      return $operator.parent('li').append(input);
    });
  };

  $(function() {
    var all_state_selects;
    $('ul.switches li select[name=state]').change(function() {
      return ensure_correct_visibility_for(this);
    });
    $('select[name$="operator"]').change(function() {
      return handle_operator_for(this);
    });
    all_state_selects = $('ul.switches li select[name=state]');
    return ensure_correct_visibility_for(all_state_selects);
  });

}).call(this);
