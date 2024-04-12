def get_js_template(command, view, button_type, module, name, entity):
    if command == "button":
        converted_name = name.capitalize().replace('-', '')
        if view == "list" and button_type == "mass-action":
            return generate_mass_action_template(module, entity, name, converted_name)
        else:
            return generate_button_template(module, entity, name, converted_name)
    else:
        # Add templates for other commands here
        return ""


def generate_mass_action_template(module, entity, name, converted_name):
    return f"""
define('{module}:handlers/{entity}/{name}-handler', [], function () {{

  var {converted_name}Handler = function (view) {{
    this.view = view;
  }};

  _.extend({converted_name}Handler.prototype, {{

    init{converted_name} () {{
      // called when the list view is loaded
    }},

    action{converted_name} (data) {{
      console.log(data); // data to be sent to the back-end
    }}

  }});

  return {converted_name}Handler;
}});
"""


def generate_button_template(module, entity, name, converted_name):
    return f"""
define('{module}:handlers/{entity}/{name}-handler', ['action-handler'], function (Dep) {{

  return class extends Dep {{

    action{converted_name} (data, e) {{
      Espo.Ajax
        .getRequest('{entity.capitalize()}/' + this.view.model.id)
        .then(response => {{
          console.log(response);
        }});
    }}

    init{converted_name} () {{
      this.controlButtonVisibility();

      this.view.listenTo(
        this.view.model,
        'change:status',
        this.controlButtonVisibility.bind(this)
      );
    }}

    controlButtonVisibility () {{
      if (~['Converted', 'Dead', 'Recycled'].indexOf(this.view.model.get('status'))) {{
        this.view.hideHeaderActionItem('{name}');
        return;
      }}

      this.view.showHeaderActionItem('{name}');
    }}
  }};
}});
"""