(function () {

    /** To prevent a form submitting again when refresh **/

    String.prototype.setTokens = function (replacePairs, callBack = new Function) {

        let str = this.toString(), key, re;

        for (key in replacePairs) {

            if (!isNaN(key)) key = "\\" + key;

            re = new RegExp("\{" + key + "\}", "gm");
            str = str.replace(re, replacePairs[key]);

            if (typeof callBack !== "function") continue;

            callBack.prototype.constructor({
                current: key,
                isEqual: re,
                value: str
            });


        }
        return str;

    };


    if (window.history.replaceState) {
        window.history.replaceState(null, null, window.location.href)
    }

    String.prototype.capitalize = function () {
        return this.charAt(0).toUpperCase() + String(this.slice(1)).toLowerCase();
    }

    String.prototype.capitalizeAll = function () {
        return this.replace(/(?:^|\s)\S/g,function(a) { return a.toUpperCase() })
    }

    String.prototype.ucwords = function () {
        return this.replace(/(?:^|\s)\S/g, function (a) {
            return a.toUpperCase();
        });
    }


    String.prototype.valid_selector_jquery = function () {
        const value = String(this).trim();
        if (typeof(value) !== 'string') return false;
        try {
            const element = jQuery(value);
            return true;
        }
        catch(error) { return false; }
    }

    window.define_const = function (name, value, property = window) {

        Object.defineProperty(property, name, {
            value: value,
            enumerable: true,
            configurable: true,
            writable: false
        });

    };

    window.define_value = function (name, value, property = window) {

        Object.defineProperty(property, name, {
            value: value,
            enumerable: true,
            configurable: true,
            writable: true
        });

    };

    define_const("serialize_form", function () {

        const self = this[0];
        const nodeName = self.nodeName;

        if (nodeName !== "FORM")
            throw new Error("Invalid node");

        if (this.length > 1)
            throw new Error("Invalid length of node");

        const serialize = this.serializeArray();
        const obj = {};

        serialize.forEach(function (value) {
            obj[value.name] = value.value;
        });

        return obj;


    }, $.fn);

    if (jQuery.fn.hasOwnProperty("expandable"))
    {
        jQuery('.read_more_toggle').expandable({
         'height': 100
        });
    }


    (function() {

        // Javascript to enable link to tab
        var url = document.location.toString();
        if (url.match('#')) {
            if(!jQuery.fn.hasOwnProperty("tab")) return;
            $('.nav-tabs a[href="#' + url.split('#')[1] + '"]').tab('show');
        }

        // Change hash for page-reload
        $('.nav-tabs a').on('shown.bs.tab', function (e) {
            window.location.hash = e.target.hash;
        });


    })();

    const card_body_state_hide = function()
    {
        const $target = jQuery(this);
        const $parent = $target.parents(".card");
        const $body = $parent.find(".card-body");
        const $icon = $target.find("i");

        $body.slideUp();
        $icon.removeClass("fa-angle-up");
        $icon.addClass("fa-angle-down");

        jQuery($target).off("click").on("click",function() {
            $body.slideDown();
            $icon.removeClass("fa-angle-down");
            $icon.addClass("fa-angle-up");
            jQuery($target).off("click").on("click",card_body_state_hide);
        });

    }

    jQuery("button.cad_body_state")
        .off("click")
        .on("click",card_body_state_hide);

    window.card_body_state = function()
    {
        console.log(this);
        debugger;
    }




})();

