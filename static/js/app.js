var fileupload = document.getElementById("fileuploadpopup");
var detail = document.getElementById("detail");
var detailInfo = document.getElementById("detail-info");
var backBtn = document.getElementById("back-btn");
var finalBtn = document.getElementById("final-btn");
var i= 0;
var currentUploadValue = '';
var currentUploadCSVId = ''
var businessNames = []
var isValidated = false

$(window).on("load", function() {
    fileupload.style.display = "block";
});

backBtn.onclick = function() {
    $('#businessNames').empty();
    $('#file').val('');
    currentUploadValue = ''
    detailInfo.style.display = "none";
    fileupload.style.display = "block";
}

finalBtn.onclick = function() {
    $('#businessNames').children('.row').each(function(e) {
        var currentPosition = e + 1
        var businessNameInArray = $('#businessTags-'+currentPosition).tagsinput('items')
        var tempObj = {
            column_name: $('#column-name-'+currentPosition).val(),
            business_name: businessNameInArray,
            type: $('#data-type-'+currentPosition).val()
        }

        if(businessNameInArray.length == 0) {
            $('#businessTagsWrapper-'+currentPosition+ ' .bootstrap-tagsinput').css({
                'background-color': 'red'
            })
        } else {
            $('#businessTagsWrapper-'+currentPosition+ ' .bootstrap-tagsinput').css({
                'background-color': 'transparent'
            })
        }

        businessNames.push(tempObj)
    })

    for(var i = 0; i < businessNames.length; i++) {
        if(businessNames[i].business_name.length == 0) {
            isValidated = false
            break
        } else {
            isValidated = true
        }
    }

    if(isValidated) {
        var sendJSON = {
            id : currentUploadCSVId,
            data: businessNames
        }

        $.ajax({
            url: "/trainer",
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            data: JSON.stringify(sendJSON),
            success: function(values) {
                console.log(values)
                detailInfo.style.display = "none";
            },
            error: function(error) {
                alert("An error occured, please try again.", error);
                detailInfo.style.display = "none";
            }
        });

        console.log('POST the Business name', sendJSON)
    }

}

function businessNameTemplate() {
    var values= currentUploadValue.column_names
    for(var i = 0; i < values.length; i++) {
        $('#businessNames').append(`
            <div class="row">
                <div class="column-value col-4">
                    <div class="form-group has-float-label">
                        <input class="form-control" id="column-name-`+(i+1)+`" type="text" value="`+values[i]+`" disabled/>
                        <label for="password">Column</label>
                    </div>
                </div>
                <div class="col-5">
                    <div class="form-group has-float-label" id="businessTagsWrapper-`+(i+1)+`">
                        <input class="tagsIpt form-control" id="businessTags-`+(i+1)+`" type="text" data-role="tagsinput" />
                        <label for="password">Business name</label>
                    </div>
                </div>
                <div class="col-3">
                    <div class="form-group has-float-label">
                        <select class="form-control custom-select" id="data-type-`+(i+1)+`">
                            <option value="categorical" selected>categorical</option>
                            <option value="continuous">continuous</option>
                        </select>
                        <label>Data type</label>
                    </div>
                </div>
            </div>
        `)

        $('#businessTags-'+(i+1)).tagsinput('add', 'Hello' )
    }
}

// File upload
$("#file").change(function() {
    var fd = new FormData();
    fd.append('file', this.files[0]);

    fileupload.style.display = "none";
    detail.style.display = "block";

    $.ajax({
        url: "/upload",
        type: "POST",
        dataType: 'json',
        processData: false,
        contentType: false,
        data: fd,
        xhr: function () {
            var xhr = $.ajaxSettings.xhr();
            if (xhr.upload) {
                xhr.upload.addEventListener('progress', function(event) {
                    var percent = 0;
                    var position = event.loaded || event.position;
                    var total = event.total;
                    if (event.lengthComputable) {
                        percent = Math.ceil(position / total * 100);
                    }
                    $(".progress-bar").css("width", + percent +"%");
                    $("#status").text(percent +"%");
                }, true);
            }
            return xhr;
        }
    }).done(function (values) {
        detail.style.display = "none";
        detailInfo.style.display = "block";
        currentUploadValue = values.data
        currentUploadCSVId = values.id;
        businessNameTemplate();
        $('.tagsIpt').tagsinput('add', 'some tag');
    }).fail(function (error) {
        alert("An error occured, please try again.", error);
    });
});

$( function() {
    var availableTags = [
      "ActionScript",
      "AppleScript",
      "Asp",
      "BASIC",
      "C",
      "C++",
      "Clojure",
      "COBOL",
      "ColdFusion",
      "Erlang",
      "Fortran",
      "Groovy",
      "Haskell",
      "Java",
      "JavaScript",
      "Lisp",
      "Perl",
      "PHP",
      "Python",
      "Ruby",
      "Scala",
      "Scheme"
    ];
    $( "#myInput" ).autocomplete({
      source: availableTags
    });
});


$("#myInput").keypress(() => {
    $("#myInput").addClass("intro");
    $("#ui-id-1").css("border-top", "0px");
})
