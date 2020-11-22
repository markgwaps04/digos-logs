(function(jq) {
    $element = jq(".activity_list");
    $element.jsGrid({
//      pagerContainer: jq(".q_pagination"),
      inserting: false,
      editing: false,
      filtering: false,
      height: "90%",
      width: "100%",
      heading: false,
      paging: true,
      autoload: true,
      pageSize: 10,
      paging:true,
      pageLoading:true,
      pageIndex:1,
      controller: {
        loadData : function(filter)
        {
            const send = jq.ajax({
                url : "/teacher/activity/list/request?group=" + window.fn_group,
                headers: {"X-CSRFToken": jq.cookie("csrftoken")},
                data : {...{search : ""},...filter},
                type : "post"
            });

            return new Promise(function(resolve) {
                send.done(function(response) {
                    const $element = jq(response);
                    const length = $element.attr("item_count");

                    if(!length)
                        return resolve({
                            data: [],
                            itemsCount: length
                        });

                    resolve({
                        data: [response],
                        itemsCount: length
                    });

                });
            });

        }
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
          '<a href="/teacher/activity/add?group='+window.fn_group+'">' +
          'Click this link to add new activity' +
          '</a>' +
          '</p>');

        container.append(per);

        return container;


      }
    });

    $form = jq("form#activity_search");

    $form.keyup(function() {
       const values = $form.serialize_form();
       const loadSpinner = jq(".input-group-prepend").removeClass("hidden");
       const send = $element.jsGrid("loadData",values);
       send.then(function() {
           loadSpinner.addClass("hidden");
       })
    });

    $form.submit(function(e) {
        e.preventDefault();
    });

})(jQuery);
