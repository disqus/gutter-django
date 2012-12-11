(function() {
  var add_condition_to, attr_setter, ensure_correct_arguments_for, ensure_correct_visibility_for, recalculate_condition_attrs_for, remove_condition, swtch;

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

  attr_setter = function(attr_name, number) {
    return function(index, element) {
      var name_parts;
      name_parts = $(element).attr(attr_name).split('-');
      name_parts[1] = number + 1;
      return $(element).attr(attr_name, name_parts.join('-'));
    };
  };

  add_condition_to = function(row) {
    var clone, prototype;
    prototype = $(row).find('ul.conditions li:last-child').first();
    clone = prototype.clone(true, true);
    prototype.parent('ul.conditions').append(clone);
    clone.find('input,select').removeAttr('selected').attr('value', '');
    return recalculate_condition_attrs_for(row);
  };

  remove_condition = function(condition) {
    var row;
    row = $(condition).parents('ul.switches li');
    $(condition).remove();
    return recalculate_condition_attrs_for(row);
  };

  recalculate_condition_attrs_for = function(row) {
    var condition_rows;
    return condition_rows = $(row).find('ul.conditions li').each(function(index, element) {
      $(element).find('input,select').map(attr_setter('name', index));
      $(element).find('input,select').map(attr_setter('id', index));
      return $(element).find('label').map(attr_setter('for', index));
    });
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
      row = $(event.currentTarget).parents('li')[0];
      return add_condition_to(row);
    });
    $('ul.switches li section.conditions button[data-action=remove]').click(function(event) {
      var condition;
      event.preventDefault();
      condition = $(event.currentTarget).parents('li')[0];
      return remove_condition(condition);
    });
    return $.map($('ul.switches li'), ensure_correct_visibility_for);
  });

}).call(this);
