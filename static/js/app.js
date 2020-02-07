var fileupload = document.getElementById("fileuploadpopup");
var detail = document.getElementById("detail");
var detailInfo = document.getElementById("detail-info");
var backBtn = document.getElementById("back-btn");
var finalBtn = document.getElementById("final-btn");
var i= 0;
var searchValue;
var currentUploadValue = '';
var currentUploadCSVId = ''
var businessNames = []
var isValidated = false
var searchQuestion= '';

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
            $('#businessTagsWrapper-'+currentPosition).css({
                'border-bottom': '1px solid red'
            })
            $('#businessTagsWrapper-'+currentPosition+ ' .error-label').css({
                'color': 'red'
            })
        } else {
            $('#businessTagsWrapper-'+currentPosition).css({
                'border-bottom': '1px solid #E5E5E5'
            })
            $('#businessTagsWrapper-'+currentPosition+ ' .error-label').css({
                'color': '#b1acac'
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
                questionsTemplate(values.questions)
            },
            error: function(error) {
                alert("An error occured, please try again.", error);
            }
        });

        console.log('POST the Business name', sendJSON)
    }
}

function businessNameTemplate() {
    var values= currentUploadValue.column_names
    for(var i = 0; i < values.length; i++) {
        $('#businessNames').append(`
            <div class="row mb-1">
                <div class="column-value col-4">
                    <div class="border-0 form-group has-float-label">
                        <input class="form-control w-100" id="column-name-`+(i+1)+`" type="text" value="`+values[i]+`" disabled/>
                        <label>Column</label>
                    </div>
                </div>
                <div class="col-5">
                    <div class="form-group has-float-label error-div" id="businessTagsWrapper-`+(i+1)+`">
                        <input class="tagsIpt form-control" id="businessTags-`+(i+1)+`" type="text" data-role="tagsinput" />
                        <label class="error-label">Business name</label>
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

function questionsTemplate(value) {
    $('#questionsTemp').append(`<p>Suggestion:</p>`)
    for(var i = 0; i < value.length; i++) {
        $('#questionsTemp').append(`
            <button class="questions-btn" id="questions-`+ i +`">`+ value[i] +`</button>
        `);
        buttonClick(i)
    }
}

function buttonClick(index) {
    $("#questions-"+ index).click(function() {
        var consoleValue = $(this).text();
        console.log(consoleValue);
        $('input[name="searchValue"]').val(consoleValue);
    })
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

$(document).ready(function() {
    $('#myInput').keyup(function(e) {
        searchValue= $(this).val()
        var dataset= '{"data": "'+ searchValue +'", "id": "'+ currentUploadCSVId +'"}';
        console.log(dataset);
        $.ajax({
            url: "/search",
            type: "POST",
            dataType: 'json',
            contentType: 'application/json',
            data: dataset,
            success: function(resp) {
                console.log(resp.questions)                
                var availableTags = resp.questions;
                $( "#myInput" ).autocomplete({
                    source: availableTags,
                    open: function( event, ui ) {
                        $("#myInput").addClass("intro");
                        $("#ui-id-1").css("border-top", "0px");
                    },
                    close: function(event, ui) {
                        $("#myInput").removeClass("intro");
                    }
                });
                
            }
        })
        if(e.which == 13) {
            var dataEnter = '{"data": "'+ searchValue +'", "id": "'+ currentUploadCSVId +'"}';
            $.ajax({
                url: "/chart_finder",
                type: "POST",
                dataType: 'json',
                contentType: 'application/json',
                data: dataEnter,
                success: function(resp) {
                    console.log(resp.questions);
                    searchValue = $(this).val('');
                }
            })
        }
    })
})