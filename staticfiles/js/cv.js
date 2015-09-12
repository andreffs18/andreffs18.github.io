/**
 * Created by andresilva on 8/15/15.
 */
String.prototype.capitalizeFirstLetter = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
};

var build_row = function(rows, i){
    var row = "";
    rows.forEach(function(el){
        row += '<div class="row"> \
                    <div class="col-md-6">\
                        <h4 class="text-left text-md-right">' + el.period + '</h4> \
                        <h5 class="text-left text-md-right">' + el.place + '</h5> \
                    </div> \
                    <div class="col-md-6 text-left description">' + el.description + '</div> \
                </div>';
    });
    return row
};

var build_section = function(section, i){
    var sections = "";
    $.each(section, function(field, rows){
        sections += '<div class="row section"> \
                        <div class="col-md-2"> \
                            <h3 class="text-uppercase">' + field.toUpperCase() + '</h3>\
                        </div> \
                        <div class="col-md-10">' + build_row(rows, i) + '</div> \
                    </div>';
    });
    return sections
};


$(document).ready(function(){
    //var cv = JSON.parse($('input[type="hidden"][name="cv"]').val());
    var html = "";
    cv.forEach(function(el, index){
        console.log("Building cv section \"" + el+ "\"");
        html += build_section(el, index);
    });

    $('div.cv-placeholder').append(html);
});