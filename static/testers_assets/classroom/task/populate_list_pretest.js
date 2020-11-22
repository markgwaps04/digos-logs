(function(jq){

const $element = jq(".task_add_batch_modal .jsgrid");

    $element.jsGrid({
      inserting: false,
      editing: false,
      filtering: false,
      height: "90%",
      width: "100%",
      heading: false,
      paging: true,
      autoload: true,
      pageSize: 3,
      paging:true,
      pageLoading:true,
      pageIndex:1,
      controller: {
        loadData : function(filter)
        {
            filter.search = filter.search || "";
            filter.section = window.fn_section;
            filter.batch = fn_batch;
            filter.test_type = window.fn_test_type;

            const send = jq.ajax({
                url : "/teacher/task/list/pre/activity/load",
                headers: {"X-CSRFToken": jq.cookie("csrftoken")},
                data : filter,
                type : "post"
            });

            return new Promise(function(resolve) {

                send.done(function(response) {
                    const $element = jq(response);
                    const length = $element.attr("item_count");

                    if(!length) return resolve({data : [],itemsCount : 0});

                    resolve({data: [response],itemsCount: length});

                });
            });

        }
      },
      loadIndicator : {
        show : () => jq(".task_add_batch_modal .overlay-spinner").addClass("show"),
        hide : () => jq(".task_add_batch_modal .overlay-spinner").removeClass("show")
      },
      rowRenderer : function(template)
      {
         const of_template = jQuery(template);
         const more_link = of_template.find(".more");

         if (more_link.length) more_link.read_more(100);
         return of_template;
      },
      noDataContent: function () {
        const container = jq("<div>");
        container.addClass("inner_content");
        container.css("padding","30px");

        const per = jq("<div>");
        container.addClass("no_display");

        const title = jq("<h4>");
        title.html("No display");

        per.append(title);
        per.append('<p>' +
          '<span>'+
          'We cant find any information or source' +
          '</span>' +
          '</p>');

        container.append(per);

        return container;

      }
    });

    const $form = jq(".task_add_batch_modal form#search");

    $form.keyup(function() {
       const values = $form.serialize_form();
       const send = $element.jsGrid("search",values);
    });

    $form.submit(function(e) {
        e.preventDefault();
    });

})(jQuery);
