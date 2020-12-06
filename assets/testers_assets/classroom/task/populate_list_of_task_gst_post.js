(function(jq) {


    const $element = jq(".list_task .jsgrid");
    $element.jsGrid({
      inserting: false,
      editing: false,
      filtering: false,
      height: "90%",
      width: "100%",
      heading: false,
      paging: true,
      autoload: true,
      pageSize: 6,
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
                url : "/teacher/task/list/load",
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
        show : () => jq(".list_task .overlay-spinner").addClass("show"),
        hide : () => jq(".list_task .overlay-spinner").removeClass("show")
      },
      rowRenderer : function(template)
      {
         return jQuery(template);
      },
      noDataContent: function () {
        const container = jq("<div>");
        container.addClass("inner_content")

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


    const $form = jq(".list_task form.search");

    $form.keyup(function() {
       const values = $form.serialize_form();
       const send = $element.jsGrid("search",values);
    });

    $form.submit(function(e) {
        e.preventDefault();
    });

})(jQuery);
