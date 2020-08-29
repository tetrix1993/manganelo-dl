let $selectSeries = $('#select-series');
let $selectChapter = $('#select-chapter');
let $divImages = $('#div-images');
let $btnTop = $('#btn-top');

let seriesList; // object
let chapterList; // object
let imagesList;

let currSeries;
let currSeriesId = -1;

let currChapter;
let currChapterName = '';

function enable_waiting_cursor() {
    $('html').addClass('waiting');
}

function disable_waiting_cursor() {
    $('html').removeClass('waiting');
}

function disable_waiting_cursor_after_image_load(total_image) {
    var loaded = 0;
    $('img').on('load', function() {
        loaded += 1;
        if (loaded == total_image)
            disable_waiting_cursor();
    });
}

function selectSeries(obj) {
    currSeriesId = obj.value;
    if (currSeriesId == -1) {
        $divImages.html('');
        $selectChapter.html('');
        currChapterName = '';
        currSeries = {};
        chapterList = {}
        imagesList = {};
        $btnTop.hide();
    } else {
        currSeries = seriesList[currSeriesId];
        loadChapter();
        $btnTop.show();
    }
}

function selectChapter(obj) {
    chapter_id = obj.value;
    currChapter = chapterList[chapter_id];
    currChapterName = currChapter.name;
    loadImages();
}

function loadFirstChapter() {
    currChapter = chapterList[0];
    currChapterName = currChapter.name;
    loadImages();
}

function loadImages() {
    enable_waiting_cursor();
    $.ajax('/download/' + currSeries.id + '/' + currChapter.url + '/data.json', {
        success: function(data) {
            imagesList = data
            $divImages.html('<br/>');
            timenow = performance.now()
            i = 0;
            for (i = 0; i < imagesList.length; i++) {
                $divImages.html($divImages.html() + '<div class="image"><img src="download/' + currSeries.id + '/' + currChapter.url + '/' + imagesList[i] + '?' + timenow + '" /></div>');
            }
            if (i == imagesList.length) {
                disable_waiting_cursor_after_image_load(imagesList.length);
            }
            if (imagesList.length == 0)
                disable_waiting_cursor();
        },
        error: function(data, textStatus, xhr) {
            alert(data.status + ' ' + xhr);
            disable_waiting_cursor();
        }
    });
}

let loadSeries = function() {
    enable_waiting_cursor();
    $.ajax('/static/data.json', {
        success: function(data) {
            seriesList = data;
            for (i = 0; i < seriesList.length; i++) {
                series = seriesList[i]
                $selectSeries.html($selectSeries.html() + '<option value="' + i + '">' + series.name + '</option>');
            }
            disable_waiting_cursor();
        },
        error: function(data, textStatus, xhr) {
            alert(data.status + ' ' + xhr);
            disable_waiting_cursor();
        }
    });
}

let loadChapter = function() {
    enable_waiting_cursor();
    seriesId = currSeries.id;
    $.ajax('/download/' + seriesId + '/data.json', {
        success: function(data) {
            chapterList = data;
            $selectChapter.html('');
            for (i = 0; i < chapterList.length; i++) {
                $selectChapter.html($selectChapter.html() + '<option value="' + i + '">' + chapterList[i].name + '</option>');
            }
            loadFirstChapter();
        },
        error: function(data, textStatus, xhr) {
            alert(data.status + ' ' + xhr);
            disable_waiting_cursor();
        }
    });
    /*let xhr = new XMLHttpRequest();
    xhr.open('GET', '/static/json/' + seriesId + '.json');
    xhr.onload = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            imagesList = JSON.parse(xhr.responseText);
            $selectPage.html('');
            for (i = 0; i < imagesList.length; i++) {
                $selectPage.html($selectPage.html() + '<option value="' + i + '">Page ' + (i+1) + '</option>');
            }
            loadFirstImage();
            //loadHiddenImages();
        } else {
            alert('Error - ' + xhr.status);
        }
    }
    xhr.send();*/
}

function scrollToTop()
{
    document.body.scrollTop = 0; // For Safari
    document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

$(document).ready(function() {
    loadSeries();
});
