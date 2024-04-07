def get_js_template(command, view, button_type, module, name, entity):
    if command == "button":
        if view == "list" and button_type == "mass-action":
            return f"""
define('{module}:{name}-handler', [], function () {{

  var {name.capitalize()}Handler = function (view) {{
    this.view = view;
  }};

  _.extend({name.capitalize()}Handler.prototype, {{

    init{name.capitalize()}: function () {{
      // called when the list view is loaded
    }},

    action{name.capitalize()}: function (data) {{
      console.log(data); // data to be sent to the back-end
    }},

  }});

  return {name.capitalize()}Handler;
}});
"""
        else:
            return f"""
define('{module}:{name}-handler', ['action-handler'], function (Dep) {{

  return Dep.extend({{

    action{name.capitalize()}: function (data, e) {{
      Espo.Ajax
        .getRequest('{entity.capitalize()}/' + this.view.model.id)
        .then(response => {{
          console.log(response);
        }});
    }},

    init{name.capitalize()}: function () {{
      this.controlButtonVisibility();

      this.view.listenTo(
        this.view.model,
        'change:status',en
        this.controlButtonVisibility.bind(this)
      );
    }},

    controlButtonVisibility: function () {{
      if (~['Converted', 'Dead', 'Recycled'].indexOf(this.view.model.get('status'))) {{
        this.view.hideHeaderActionItem('{name}');
        return;
      }}

      this.view.showHeaderActionItem('{name}');
    }},
  }});
}});
"""
    else:
        # Add templates for other commands here
        return ""