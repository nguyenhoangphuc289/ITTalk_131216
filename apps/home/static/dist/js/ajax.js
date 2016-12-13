/**
 * Created by phuc on 27/11/2016.
 */
var feedsOffset = 0;
var feedLoader = function () {
    $.ajax({
        url: '/ajax/feeds/?offset=' + feedsOffset,
        success: function (data) {
            if (data.length > 0) {
                $('#results').append(data);
                feedsOffset += 5
            } else {
                $('#load_more').hide();
            }
        }
    });
};
$('#load_more').click(function () {
    feedLoader();
});
feedLoader();

var deletePost = function (id) {
    $.ajax({
        url: '/ajax/delete/?id=' + id,
        success: function () {
            $('#item_' + id).slideUp();
            feedsOffset -= 1;
        }
    });
};

var deleteComment = function (id) {
    $.ajax({
        url: '/ajax/deletecomment/?id=' + id,
        success: function () {
            $('#comment_' + id).slideUp();
            setTimeout(function () {
                $('#comment_' + id).remove();
            }, 1000);
        }
    });
};

$(document).on('click', '.delete_post', function () {
    $('[data-toggle="dropdown"]').parent().removeClass('open');
    var id = $(this).attr("data");
    $('#deleteModal').attr("data-delete", id);
    $('#deleteModal').modal("show");
});

$(document).on('click', '.delete_comment', function () {
    if (confirm("Bạn chắc chắn muốn xóa câu trả lời này chứ?")) {
        var id = $(this).attr("data");
        deleteComment(id);
    }
});

$(document).on('click', '#allow_delete', function () {
    var id = $(this).parents('#deleteModal').attr('data-delete');
    $('#deleteModal').modal("hide");
    deletePost(id);
    feedLoader();
    feedsOffset += 1;
});

var dislike = function (id) {
    $.ajax({
        url: '/ajax/dislike/?id=' + id,
        success: function () {
            $('#show_' + id).hide();
            $('#hide_' + id).show();
        }
    });
};

var undislike = function (id) {
    $.ajax({
        url: '/ajax/undislike/?id=' + id,
        success: function () {
            $('#show_' + id).show();
            $('#hide_' + id).hide();
        }
    });
};

$(document).on('click', '.downvote', function () {
    var id = $(this).attr("data-id");
    dislike(id);
});

$(document).on('click', '.undo', function () {
    var id = $(this).attr("data-id");
    undislike(id);
});

var wrapper;

$(document).on('click', '.edit_comment', function () {
    var container = $(this).parents('.answer_container');
    wrapper = container.parent();
    var content = container.find('.render_text');
    var editor = $(this).parents('.answer_wrapper').find('.ql-editor');
    var is_update = $(this).parents('.answer_wrapper').find('input[name=is_update]');
    var btn = $(this).parents('.answer_wrapper').find(':submit');
    btn.html('Chỉnh sửa');
    is_update.val(wrapper.attr('id').split('_')[1]);
    editor.html($.trim(content.html()));
    container.remove();
});


<!-- Event submit comment -->
$(document).on('submit', '.form_comment', function () {
    //Get panel-body - which contain comments
    var panel = $(this).parents('.answer_wrapper').find('.panel-body');
    //Get container (big panel) to display this when submit first comment
    //Container is null so do not have any comment -> must append  container into answer_wrapper
    var container = $(this).parents('.answer_wrapper');
    //Get editor - which contain comment's content
    var editor = $(this).find('.ql-editor');
    //Get hidden input contain above editor's content
    var content = $(this).find('input[name=content]');
    //Set hidden value is editor's html text
    content.val(editor.html());
    //Call ajax to function ajax_answer_question in views.py
    //with data is submitted from form (JSON format)
    //and if success so prepend comment just added to panel-body
    var is_update = $(this).find('input[name=is_update]');
    var btn = $(this).find(':submit');
    if (is_update.val() == '0') {
        $.ajax({
            type: "POST",
            url: '/ajax/answer/',
            data: $(this).serialize(),
            success: function (data) {
                content.value = ""; //Clear hidden input value
                if (panel.length) {
                    panel.prepend(data);
                } else {
                    container.append("<div class='answer-panel panel panel-default'><div class='panel-body'></div></div>");
                    var pn = container.find('.panel-body');
                    pn.append(data);
                }
                editor.html(""); //Clear editor content
            }
        });
    } else {
        $.ajax({
            type: "POST",
            url: '/ajax/answer/',
            data: $(this).serialize(),
            success: function (data) {
                content.value = ""; //Clear hidden input value
                wrapper.replaceWith(data);
                is_update.val("0");
                btn.html('Gửi');
                editor.html(""); //Clear editor content
            }
        });
    }
    return false; //Prenvent form to default, not reload page
});

$(document).on('submit', '.form_comment_post', function () {
    var answer_panel = $(this).parent();
    var container = answer_panel.find('.panel-body');
    var is_update = $(this).find('input[name=is_update]');
    var txt = $(this).find('input[name=content]');
    var btn = $(this).find(':submit');
    if (is_update.val() == '0') {
        $.ajax({
            type: "POST",
            url: '/ajax/answer/',
            data: $(this).serialize(),
            success: function (data) {
                txt.val("");
                if (container.length) {
                    container.prepend(data);
                } else {
                    answer_panel.append("<div class='panel-body'></div>");
                    var pn = answer_panel.find('.panel-body');
                    pn.append(data);
                }
            }
        });
    } else {
        $.ajax({
            type: "POST",
            url: '/ajax/answer/',
            data: $(this).serialize(),
            success: function (data) {
                content.value = ""; //Clear hidden input value
                wrapper.replaceWith(data);
                is_update.val("0");
                btn.html('Gửi');
                editor.html(""); //Clear editor content
            }
        });
    }
    return false; //Prenvent form to default, not reload page
});

$(document).on('submit', '.form_reply', function () {
    var container = $(this).parents('.cmt_name').find('.reply_wrapper');
    var txt = $(this).find('input[name=reply_content]');
    $.ajax({
        type: "POST",
        url: '/ajax/reply/',
        data: $(this).serialize(),
        success: function (data) {
            container.prepend(data);
            txt.val('');
        }
    });
    return false;
});

$(document).on('click', '.upvote_comment', function () {
    var id = $(this).parents('.form_reply').find('input[name=parent_id]').val();
    var parent = $(this).parent();
    var downvote_container = $(this).parent().parent().children('.btn').eq(1);
    $.ajax({
        url: '/ajax/upvotecomment/?id=' + id,
        dataType: 'json',
        success: function (data) {
            if (data.status == "up") {
                parent.html("<span class='text-primary upvote_comment'>Bỏ Upvote (" + data.up_count + ")</span>");
                downvote_container.html("<span class='text-muted downvote_comment'>Downvote (" + data.down_count + ")</span>");
            } else {
                parent.html("<span class='text-muted upvote_comment'>Upvote (" + data.up_count + ")</span>");
            }
        }
    });
});

$(document).on('click', '.downvote_comment', function () {
    var id = $(this).parents('.form_reply').find('input[name=parent_id]').val();
    var parent = $(this).parent();
    var upvote_container = $(this).parent().parent().find('.btn').first();
    $.ajax({
        url: '/ajax/downvotecomment/?id=' + id,
        dataType: 'json',
        success: function (data) {
            if (data.status == "down") {
                parent.html("<span class='text-primary downvote_comment'>Bỏ Downvote (" + data.down_count + ")</span>");
                upvote_container.html("<span class='text-muted upvote_comment'>Upvote (" + data.up_count + ")</span>");
            } else {
                parent.html("<span class='text-muted downvote_comment'>Downvote (" + data.down_count + ")</span>");
            }
        }
    });
});

$(document).on('click', '.btn_follow_post', function () {
    var id = $(this).parents('.form_reply').find('input[name=parent_id]').val();
    var parent = $(this).parent();
    var upvote_container = $(this).parent().parent().find('.btn').first();
    $.ajax({
        url: '/ajax/downvotecomment/?id=' + id,
        dataType: 'json',
        success: function (data) {
            if (data.status == "down") {
                parent.html("<span class='text-primary downvote_comment'>Bỏ Downvote (" + data.down_count + ")</span>");
                upvote_container.html("<span class='text-muted upvote_comment'>Upvote (" + data.up_count + ")</span>");
            } else {
                parent.html("<span class='text-muted downvote_comment'>Downvote (" + data.down_count + ")</span>");
            }
        }
    });
});

$(document).on('click', '.upvote_post', function () {
    var _this = $(this);
    var id = $(this).parents('.item').find('input[name=post_id]').val();
    var count_span = $(this).find('.upvote_count');
    $.ajax({
        url: '/ajax/like/?id=' + id,
        dataType: 'json',
        success: function (data) {
            if (data.status == "up") {
                _this.html("<i class='fa fa-thumbs-o-down'></i> Bỏ Upvote&nbsp;|&nbsp;<span class='upvote_count'></span>");
                _this.find('.upvote_count').html(data.count);
            } else {
                _this.html("<i class='fa fa-thumbs-o-up'></i> Upvote&nbsp;|&nbsp;<span class='upvote_count'></span>");
                if (data.count)
                    _this.find('.upvote_count').html(data.count);
                else
                    _this.find('.upvote_count').html("0");
            }

        }
    });
});