(function() {
  var add_condition, add_operator_arguments, adjust_submit_visibility, recalculate_condition_attrs, recalculate_total_forms, remove_condition, remove_operator_arguments, swtch, update_conditions_visibility;

  swtch = {
    disabled: '1',
    selective: '2',
    global: '3'
  };

  update_conditions_visibility = function(event) {
    var $conditions;
    $conditions = $(this).parents('ul.switches li').find('section.conditions');
    switch ($(this).val()) {
      case swtch.disabled:
      case swtch.global:
        return $conditions.hide();
      case swtch.selective:
        return $conditions.show();
    }
  };

  remove_operator_arguments = function(event) {
    return $(event.target).siblings('input[type=text]').remove();
  };

  add_operator_arguments = function(event) {
    var $operator, name_prefix, new_arguments;
    $operator = $(event.target);
    name_prefix = $operator.attr('name').split('-').slice(0, 2).join('-');
    new_arguments = $operator.find('option:selected').data('arguments').split(',');
    return $.each(new_arguments, function(index, argument) {
      var input, label, new_attrs;
      new_attrs = {
        name: name_prefix + '-' + argument,
        type: 'text',
        id: 'id_' + name_prefix + '-' + argument,
        "class": 'added'
      };
      input = $('<input>').attr(new_attrs);
      label = $('<label>').attr({
        "for": new_attrs.id
      }).text(argument);
      return $operator.parent('section.condition').append(label).append(input);
    });
  };

  add_condition = function(event) {
    var $conditions, $prototype;
    $conditions = $(this).parents('ul.switches > li').find('ul.conditions');
    $prototype = $('ul#condition-form-prototype li').first();
    $prototype.clone(true, true).appendTo($conditions);
    $conditions.find('li').last().find('input,select').removeAttr('selected').attr('value', '');
    $(this).trigger('gutter.switch.conditions.changed');
    return false;
  };

  remove_condition = function(event) {
    var $conditions;
    $conditions = $(this).parents('ul.conditions');
    $(this).parents('ul.conditions li').remove();
    $conditions.trigger('gutter.switch.conditions.changed');
    return false;
  };

  recalculate_condition_attrs = function(event) {
    var attr_setter, condition_rows;
    attr_setter = function(attr_name, number) {
      return function(index, element) {
        var name_parts;
        name_parts = $(element).attr(attr_name).split('-');
        name_parts[1] = number;
        return $(element).attr(attr_name, name_parts.join('-'));
      };
    };
    return condition_rows = $(this).find('ul.conditions li').each(function(index, element) {
      $(element).find('input,select').map(attr_setter('name', index));
      $(element).find('input,select').map(attr_setter('id', index));
      return $(element).find('label').map(attr_setter('for', index));
    });
  };

  recalculate_total_forms = function(event) {
    var count;
    count = $(this).find('ul.conditions li').length;
    $(this).find('input[name$=TOTAL_FORMS]').val(count);
    return false;
  };

  adjust_submit_visibility = function(event) {
    var inputs_and_selects;
    inputs_and_selects = $(this).find('ul.conditions').find('input,select');
    if (inputs_and_selects.not('[value]').length > 0) {
      $(this).find('input[type=submit]').attr({
        disabled: true
      });
    } else {
      $(this).find('input[type=submit]').attr({
        disabled: false
      });
    }
    return false;
  };

  $(function() {
    $('ul.switches > li').delegate('select[name=state]', 'change', update_conditions_visibility);
    $('ul.switches > li').delegate('select[name$=operator]', 'change', remove_operator_arguments);
    $('ul.switches > li').delegate('select[name$=operator]', 'change', add_operator_arguments);
    $('ul.switches > li').delegate('button[data-action=add]', 'click', add_condition);
    $('ul.switches > li').delegate('button[data-action=remove]', 'click', remove_condition);
    $('ul.switches > li').live('gutter.switch.conditions.changed', recalculate_condition_attrs);
    $('ul.switches > li').live('gutter.switch.conditions.changed', recalculate_total_forms);
    $('ul.switches > li').live('gutter.switch.conditions.changed', adjust_submit_visibility);
    $('ul.switches > li').delegate('input,select', 'blur change keypress', function() {
      return $(this).trigger('gutter.switch.conditions.changed');
    });
    $('button.addSwitch').click(function() {
      var inputs, new_switch;
      new_switch = $('ul.switches > li#switch-__new__').show();
      inputs = new_switch.find('ul.conditions').find('input,select');
      inputs.removeAttr('selected').attr('value', '');
      new_switch.trigger('gutter.switch.conditions.changed');
      return false;
    });
    $('ul.switches').find('input[name=delete],label[for=id_delete]').hide();
    $('<button data-action="delete">Delete Switch</button>').appendTo('form section.actions');
    $('button[data-action=delete]').click(function() {
      return $(this).parents('form').find('input[name=delete]').attr({
        checked: 'checked'
      });
    });
    $('ul.switches li#switch-__new__').hide();
    return $('ul.switches > li select[name=state]').trigger('change');
  });

}).call(this);
