(function() {
  var ensure_correct_visibility_for, handle_operator_for, swtch;

  swtch = {
    disabled: '1',
    selective: '2',
    global: '3'
  };

  ensure_correct_visibility_for = function(selects) {
    var conditions;
    conditions = $(selects).parents('li').find('div..conditions');
    switch ($(selects).val()) {
      case swtch.disabled:
      case swtch.global:
        return conditions.hide();
      case swtch.selective:
        return conditions.show();
    }
  };

  handle_operator_for = function(operator) {
    var args;
    args = $(operator).find('option:selected').data('arguments').split(',');
    return $.each(args)(function(index, argument) {
      var input;
      return input = $('input').attr('name', '');
    });
  };

  $(function() {
    var all_state_selects;
    all_state_selects = $('ul.switches li select[name="switch[state]"]');
    $('ul.switches li select').change(function() {
      return ensure_correct_visibility_for(this);
    });
    $('select.operator').change(function() {
      return handle_operator_for(this);
    });
    return ensure_correct_visibility_for(all_state_selects);
  });

}).call(this);
