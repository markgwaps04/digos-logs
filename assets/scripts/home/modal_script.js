
(function(jq){

const step1_form = jq("form#step1_form");
const $element = jq("form#step2_form .jsgrid");

const spinner = jq(".add_log .overlay-spinner");


const request_old_visitor_add_log = function(e) {

    const wizard = jq('#wizard-steps');
    e.preventDefault();

    try
    {
        const validation_add = jq(this)
            .parsely_custom()
            .validate({force: true});

        if(!validation_add) return false;

        const data = jq(this).serialize_form();

        const send = jq.ajax({
            url : "/log/new/request",
            headers: {"X-CSRFToken": jq.cookie("csrftoken")},
            data : data,
            type : "post",
            beforeSend : function() {
                spinner.addClass("show");
            },
            success : function() {
                spinner.removeClass("show");
            }
        });

        send.done(function(res) {

           /** after initialization of wizard **/
           wizard.trigger("reset",res);

        });


    }catch(err)
    {
        return alert('Error processing');
    }

};

const old_visitor_selected = function(e)
{
    e.preventDefault();
    const data = jq(this).serialize_form();

    /** After initialization of wizard **/

    const wizard = jq('#wizard-steps');
    const steps_api = wizard.data('plugin_Steps');
    const $step3_card = jq("#step3 .card");

    const send = jq.ajax({
      url : "/log/add/request",
      headers: {"X-CSRFToken": jq.cookie("csrftoken")},
      data : data,
      type : "post",
      beforeSend : function() {
         spinner.addClass("show");
      },
      success : function() {
         spinner.removeClass("show");
      }
    });

    send.done(function(response)
    {

        steps_api.next();
        const is_valid = String(response).valid_selector_jquery();

        if(!is_valid) return alert('Invalid response');

        const $res = jq(String(response).trim());

        const $res_forms = $res.find("form");
        $res_forms.on("submit",request_old_visitor_add_log);
        $res_forms.parsely_custom();
        $step3_card.html('');
        $step3_card.append($res);

    });

};


    $element.jsGrid({
      inserting: false,
      editing: false,
      filtering: false,
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
            const params = step1_form.serialize_form();
            const data = {...params, ...filter};

            const send = jq.ajax({
                url : "/log/search",
                headers: {"X-CSRFToken": jq.cookie("csrftoken")},
                data : data,
                type : "post",
            });

            return new Promise(function(resolve) {

                send.done(function(response)
                {

                    $element.jsGrid("_hideLoading");

                    const is_valid = String(response).valid_selector_jquery();
                    const $res_element = jq(response);
                    const length = $res_element.attr("item_count");

                    if(!length)
                    {
                        return resolve({
                            data: [],
                            itemsCount: length
                        });
                    }

                    resolve({
                        data: [response],
                        itemsCount: length
                    });

                });

            });

        }
      },
      loadIndicator : {
        show : () => jq(".add_log .overlay-spinner").addClass("show"),
        hide : () => jq(".add_log .overlay-spinner").removeClass("show")
      },
      rowRenderer : function(template)
      {

         const of_template = jQuery(template);
         const more_link = of_template.find(".more");

         const form_params = of_template.find("form.step2_old");
         form_params.on("submit", old_visitor_selected);

         if (more_link.length) more_link.read_more(100);

         return of_template;
      },
      noDataContent: function () {
        const container = jq("<div>");
        container.addClass("inner_content");

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





(function(jq) {


const step1_form = jq("form#step1_form");
const step2_new = jq("form#step2_new");
const wizard = jq('#wizard-steps');
const step3_form = jq("#step3.step-tab-panel");
const jsgrid_search = jq("form#step2_form .jsgrid");
const form_list = wizard.find("form");
const $modal = jq(".modal.add_log");
const spinner = jq(".add_log .overlay-spinner");
const modal_alert = $modal.find(".modal-header-alert");

form_list.find(".modal-footer").hide();


const step3_no_display = function() {
    const container = jq("<div>");
    container.addClass("inner_content p20");

    const per = jq("<div>");
    container.addClass("no_display");

    const title = jq("<h4>");
    title.html("No display");

    per.append(title);
    per.append(
        '<p>' +
        '<span>'+
        'We cant find any information or source' +
        '</span>' +
        '</p>'
    );

    container.append(per);
    step3_form
        .find(".card")
        .html('')
        .append(container);

};

const wizard_reset = function()
{
    const list_steps = wizard.find(".step-steps li")
          .removeClass("active")
          .removeClass("done");

    const first = jq(list_steps[0]);
    first.addClass("active");

    const first_a = first.find("a");
    const first_a_href = first_a.attr("href");

    //remove attribute 'active' all tab panel content
    const tab_panel = jq(".step-tab-panel").removeClass("active");

    const first_header = jq(".step-content").find(first_a_href);
    first_header.addClass("active");

    first_header.find(".modal-footer").css("display","flex");

};

step1_form.on("change",function() {
   const a= wizard.find(".active").nextAll();
   a.removeClass('done');
   step3_no_display();
   modal_alert.removeClass("show");
});

//setting callback function for 'hidden.bs.modal' event
$modal.on('hidden.bs.modal', function(){
  //remove the backdrop
  jq('[data-dismiss="modal"]').click();
  modal_alert.removeClass("show");
});

const steps = wizard.steps({
   onInit : function(event, currentIndex) {
       jq(form_list[0]).find(".modal-footer").show();
   },
   onChange: function(index, next, element)
   {
       const formBy_index = jq(form_list[index]);
       const stepBy_index= jq(wizard.find(".step-steps li")[index]);

       if(formBy_index.is("#step1_form"))
       {
           const validation_step1 = step1_form
            .parsley()
            .validate({force: true});

           if (!validation_step1) return false;

           return true;

       }

       if(formBy_index.is("#step2_new"))
            jsgrid_search.jsGrid("loadData");

        form_list.find(".modal-footer").hide();
        jq(form_list[next]).find(".modal-footer").show();

       return true;

   }
});

const steps_api = steps.data('plugin_Steps');

wizard.on("reset", function(event, result_modal) {

    const jsgrid_table = jq(".jsgrid.main");
    jsgrid_table.jsGrid("loadData");
    step1_form[0].reset();
    wizard_reset();
    $modal.modal("hide");

    const $result = jq(result_modal);

    $result.on("shown.bs.modal", function() {

      const removeButton = jq(this).find("#action-remove");
      const spinner =  jq(this).find(".overlay-spinner");
      form_modal = removeButton.form_modal({
            before : function(form)
            {
                if(form.is(removeButton))
                {

                    const a = vex.dialog.confirm({
                        message : "Are you sure you want to remove this log ?",
                        callback : function(value) {
                            a.options.callback(value)
                        }
                     });

                    return a;

                }
            },
            after : function(params)
            {
                if(params.$element.is(removeButton))
                {
                    $result.modal("hide");
                    vex.dialog.alert("Successfully removed");
                    jsgrid_table.jsGrid("loadData");
                }
            }

      })



    });

    $result.modal("show");
    $result.on('hidden.bs.modal', function(){
        jq('[data-dismiss="modal"]').click();
        $result.remove();
    });


    //modal_alert.html(modal_container);
    //modal_alert.addClass("show");
//    modal_alert.find(".close-modal-alert").on("click",function() {
//          modal_alert.removeClass("show");
//    });

});

jq.fn.parsely_custom = function() {

    return jq(this).parsley({
        errorsContainer : function(e)
        {
            const input_container = e.$element.parents(".input-group");
            if(e.$element.is("[type=radio]"))
                input_container.addClass('bg-error');

            return input_container.parent();

        }
    });

};

//Save and close button
const add_as_new = function(e) {
    e.preventDefault();
    try
    {
        const form_visitor_details = jq("form.visitor_details");
        const log_form_validation_add = jq(this)
            .parsely_custom()
            .validate({force: true});

        const visitor_form_validation_add = form_visitor_details
            .parsely_custom()
            .validate({force: true});

        if(!log_form_validation_add || !visitor_form_validation_add) return false;

        const log_data = jq(this).serialize_form();
        const visitor_details = form_visitor_details.serialize_form();

        const data = {...log_data, ...visitor_details};

        const send = jq.ajax({
            url : "/visitor/add/request",
            headers: {"X-CSRFToken": jq.cookie("csrftoken")},
            data : data,
            type : "post",
            beforeSend : function() {
                spinner.addClass("show");
            },
            success : function() {
                spinner.removeClass("show");
            }
        });

        send.done(function(res) {
            wizard.trigger("reset",res);
        });


    }catch(err)
    {
        return alert('Error processing');
    }

};

step1_form.submit(function(e) {
    e.preventDefault();
    steps_api.next();
    const $element = jq("form#step2_form .jsgrid");
    $element.jsGrid("loadData",jq(this).serialize_form());
});

step2_new.submit(function(e) {
    e.preventDefault();
    const $element = jq("#step3 .card");
    const step1_form_data = step1_form.serialize_form();

    const send = jq.ajax({
        url : "/visitor/add",
        headers: {"X-CSRFToken": jq.cookie("csrftoken")},
        data : step1_form_data,
        type : "post",
        beforeSend : function() {
            spinner.addClass("show");
        },
        success : function() {
            spinner.removeClass("show");
        }
     });


     send.done(function(response) {

        steps_api.next();
        const is_valid = String(response).valid_selector_jquery();

        if(!is_valid) return alert('Invalid response');

        const $res = jq(String(response).trim());
        const $res_forms = $res.find("form");
        $res_forms.on("submit",add_as_new);
        $res_forms.parsely_custom();
        $element.html('');
        $element.append($res);


     });



});

})(jQuery);



(function(jq) {


const tracing_code_form = jq("form#step1_form_code");

const form_on_submit = function(that_form)
{
    const validation_add = that_form
            .parsely_custom()
            .validate({force: true});

    if(!validation_add) return;

    const spinner = that_form.parents(".modal").find(".overlay-spinner");
    const error_template = that_form.find(".modal-header-alert_code");
    const modal = that_form.parents(".modal");

    const log_data = that_form.serialize_form();

    const send = jq.ajax({
        url : "/log/tracing_code",
        headers: {"X-CSRFToken": jq.cookie("csrftoken")},
        data : log_data,
        type : "post",
        beforeSend : function() {
            spinner.addClass("show");
            error_template.addClass("hide");
        },
        error : function() {
            spinner.removeClass("show");
        },
        success : function() {
            spinner.removeClass("show");
            error_template.addClass("hide");
        }
     });

     send.error(function() {
        error_template.removeClass("hide");
     });

     send.done(function(res) {
        modal.modal("hide");

        const $result = jq(res);
        $result.on('hidden.bs.modal', function(){
            jq('[data-dismiss="modal"]').click();
            $result.remove();
        });

        $result.modal("show");

     });


}


tracing_code_form.submit(function(e) {
    e.preventDefault();
    form_on_submit(jq(this));
});


})(jQuery)
