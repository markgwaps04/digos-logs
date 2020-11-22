(function(jq) {

    const $student_activity = jq(".student_activity");

    $student_activity.jsGrid({
        height: "100%",
        inserting: false,
        editing: false,
        filtering: false,
        width: "100%",
        paging: false,
        autoload: true,
        pageSize: 4,
        data: [],
        headerRowRenderer : null,
        filterRowRender : null,
        noDataContent : function() {

            const container = jq("<div>");
            container.addClass("app-page-title no-data");

            const sub_container = jq("<div>");
            sub_container.addClass("text-center");

            const h3 = jq("<h3>");
            h3.text("No task");
            sub_container.append(h3);

            const sub_heading = jq("<div>");
            sub_heading.addClass("page-title-subheading");
            sub_heading.text(
            "We can't find any available task at this moment or ask your teacher for help about this behaviour.");

            sub_container.append(sub_heading);
            container.append(sub_container);



            return container;

        },
        rowRenderer : function(template)
        {
             return jQuery(template);
        },
        controller: {

            loadData: function (args) {
                const send = jq.ajax({
                    method: "GET",
                    url: "/student/load/activity",
                    error: (e) => document.write(e.responseText),
                    headers: {"X-CSRFToken": jq.cookie("csrftoken")}
                });

                return new Promise(function(resolve) {
                    send.done(function(response) {
                        const $element = jq(response);
                        const length = $element.find(".section").length;
                        if(!length) return resolve([]);
                        resolve([response]);
                    });
            });
          }
        }
    });


    const refresh_grid = function()
    {
        setTimeout(function()
        {
            $student_activity.jsGrid("loadData");
            refresh_grid();
        },2000);

    };

    //refresh_grid();



})(jQuery);
