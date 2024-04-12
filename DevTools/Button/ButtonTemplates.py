class ButtonTemplates:


    @staticmethod
    def get_detail_dropdown(**kwargs):
        return ""

    @staticmethod
    def get_detail_top_right(**kwargs):
        return ""

    @staticmethod
    def get_list_mass_action(**kwargs):
        return ""

    @staticmethod
    def get_mass_action_template(**kwargs):
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

    @staticmethod
    def generate_button_template(**kwargs):
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
