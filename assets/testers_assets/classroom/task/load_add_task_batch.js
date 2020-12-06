(function(jq) {

    const $main_list = jq(".list_task .jsgrid");


    const $element = jq(".modal .jsgrid");
    $element.jsGrid({
      pagerContainer: jq(".modal #pagination"),
      inserting: false,
      editing: false,
      filtering: false,
      height: "90%",
      width: "100%",
      heading: false,
      paging: true,
      autoload: true,
      pageSize: 4,
      paging:true,
      pageLoading:true,
      pageIndex:1,
      controller: {
        loadData : function(filter)
        {
            filter.search = filter.search || "";
            filter.batch = window.fn_batch;
            filter.section = window.fn_section;
            filter.test_type = window.fn_test_type;

            const send = jq.ajax({
                url : "/teacher/task/list/add",
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

    $element.jsGrid("option","onDataLoaded", function() {

        const form_add = $element.find("form.add");

        form_add.submit(function(e) {
            e.preventDefault();

            const target = jq(this);
            const data = target.serialize_form();
            const $button = target.find("button");
            const copy_button = jq($button[0].outerHTML);

            const $ladda = Ladda.create($button[0]);

            const send = jq.ajax({
                url : "/teacher/task/list/add/request",
                headers: {"X-CSRFToken": jq.cookie("csrftoken")},
                data : data,
                dataType : "json",
                type : "post",
                beforeSend : () => $ladda.start(),
                error : e => document.write(e.responseText)
            });

            send.then(function() {
                $main_list.jsGrid("loadData");
            });

            send.done(function() {

                setTimeout(function() {

                    copy_button.removeClass("btn-info");
                    const icon = copy_button.find("i").removeClass("fa-plus");
                    icon.addClass("fa-check");
                    copy_button.attr("disabled",true).addClass("btn-success");
                    copy_button.find("span.label").html("Already added");

                    target.replaceWith(copy_button)
                    $ladda.stop();

                },1000);

            });

            $ladda.start();

        });

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
