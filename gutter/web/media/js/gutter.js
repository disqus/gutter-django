(function() {
  var add_condition_to, ensure_correct_arguments_for, ensure_correct_visibility_for, swtch;

  swtch = {
    disabled: '1',
    selective: '2',
    global: '3'
  };

  ensure_correct_visibility_for = function(row) {
    var $conditions, $select;
    $conditions = $(row).find('section.conditions');
    $select = $(row).find('select[name=state]');
    switch ($select.val()) {
      case swtch.disabled:
      case swtch.global:
        return $conditions.hide();
      case swtch.selective:
        return $conditions.show();
    }
  };

  ensure_correct_arguments_for = function(row) {
    var $operator, name_prefix, new_arguments;
    row.find('input[type=text]').remove();
    $operator = row.find('select[name$="operator"]');
    name_prefix = $operator.attr('name').split('-').slice(0, 3).join('-');
    new_arguments = $operator.find('option:selected').data('arguments').split(',');
    return $.each(new_arguments, function(index, argument) {
      var input;
      input = $('<input>').attr({
        name: name_prefix + '-' + argument,
        type: 'text'
      });
      return row.append(input);
    });
  };

  add_condition_to = function(row) {
    return event.preventDefault();
  };

  $(function() {
    var $state_selects;
    $state_selects = $('ul.switches li select[name=state]');
    $state_selects.change(function(event) {
      var row;
      row = $(this).parents('li');
      return ensure_correct_visibility_for(row);
    });
    $('select[name$="operator"]').change(function(event) {
      var row;
      row = $(this).parent('li');
      return ensure_correct_arguments_for(row);
    });
    $('ul.switches li section.conditions button[data-action=add]').click(function(event) {
      var row;
      event.preventDefault();
      row = $(event.currentTarget).parent('li')[0];
      return add_condition_to(row);
    });
    return $.map($('ul.switches li'), ensure_correct_visibility_for);
  });

}).call(this);
