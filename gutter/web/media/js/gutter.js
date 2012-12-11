(function() {
  var add_condition_to, ensure_correct_arguments_for, ensure_correct_visibility_for, increment_attr, swtch;

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

  increment_attr = function(index, attr) {
    var name_parts;
    name_parts = attr.split('-');
    name_parts[1]++;
    return name_parts.join('-');
  };

  add_condition_to = function(row) {
    var clone, list, prototype;
    prototype = $(row).find('ul.conditions li:last-child').first();
    clone = prototype.clone();
    list = prototype.parent('ul.conditions');
    clone.find('input,select').each(function(index, element) {
      $(element).attr('name', increment_attr);
      return $(element).attr('id', increment_attr);
    });
    clone.find('label').each(function(index, element) {
      return $(element).attr('for', increment_attr);
    });
    return clone.appendTo(list);
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
    return $.map($('ul.switches li'), ensure_correct_visibility_for);
  });

}).call(this);
