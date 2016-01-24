(function($) {
    $.OembedUploader = function(o) {
        this._options = {
            action = "/server/upload"

        };
        $.extend(this._options, o);

        if (this._options.button){ 
            this._button = this._createUploadButton(this._options.button);
        }
    };
    $.OembedUploader.prototype = {



    });
})(grp.jQuery);