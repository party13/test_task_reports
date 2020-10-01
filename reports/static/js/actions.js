$(document).ready(function(){
    $('#entity-form-date').daterangepicker({
        singleDatePicker: true,
        showDropdowns: true,
        minYear: 1901,
        maxYear: parseInt(moment().format('YYYY'), 10)
        }, function(start, end, label) {
            date = start.format('YYYY-MM-DD');
            console.log(date);
            $('#entity-form-date').text(date);
            $('input#date_value').val(date);
            });

    $('input.js-input-control').on('input', function(){
        $('#create_form_error_message').html('')
        dst = parseInt($('input[name="distance"]').val())
        dur = parseInt($('input[name="duration"]').val())
        if (dst  && dur  && dur!= 0){
           speed = Math.round(100 * dst / dur) / 100
           $('#average_counted_speed').find('span').text(speed)
        } else {
           $('#average_counted_speed').find('span').text('')
        }
    })

    $('#submit_create_action').click(function(){
        form = $('#new_entity')
        valid = true;
//        if (form.find('input[name="distance"]').val() == ''){
//            valid = false;
//            $('span.form-message[name^="distance"]').css('color', 'red')
//            .text('Fill this field first!')
//            .slideUp(500).fadeIn(500).delay(2000).fadeOut(500)
//        }
//        if (form.find('input[name="duration"]').val() == ''){
//            valid = false;
//            $('span.form-message[name^="duration"]').css('color', 'red')
//            .text('Fill this field first!')
//            .fadeIn(500).delay(2000).fadeOut(500)
//        }
        if (!parseInt(form.find('input[name="duration"]').val())){
            valid = false;
            $('span.form-message[name^="duration"]').css('color', 'red')
            .text('Incorrect duration!')
            .fadeIn(500).delay(2000).fadeOut(500)
        }
        if (!parseInt(form.find('input[name="distance"]').val())){
            valid = false;
            $('span.form-message[name^="distance"]').css('color', 'red')
            .text('Incorrect distance!')
            .fadeIn(500).delay(2000).fadeOut(500)
        }
        if (valid){
           createNewEntity(form)
        }
    })

    $('.js-delete-entity').on('click', function(){
        e_id = $(this).attr('js-id')
        url = $(this).attr('js-url')
        $('input#delete_entity_input').val(e_id)
        $('span#to_delete_info').text($(this).attr('js-info'))
    })

    $('.js-sort').on('click', function(){
        sort = $(this).attr('js-sort')
        console.log('sort: ' + sort)

        chk =  $(this).prop('checked')
        console.log('chk: ' + chk)

        if (chk){
            lnk = '?sort=' + sort
        } else {
            lnk = '?sort=date'
        }
        console.log('lnk: ' + lnk)
        window.location.href = lnk
    })

    $('#user_email_form').on('keyup keypress', function(e) {
        var keyCode = e.keyCode || e.which;
        if (keyCode === 13) {
            e.preventDefault();
            submitEditUserEmail();
            return false;
        }
        if (keyCode === 27) {
            default_value = $('#editable-user-email').text().replace(/\s+/g, ' ').trim();
            renderUserEmail(default_value);
            return false;
        }
        });
});

function createNewEntity(form){
    url = form.attr('js-link')
    console.log('saving....')
    $.post(url, form.serialize(),
        function(response){
            response = JSON.parse(response)
            if (response.result == true){
                $('#success_create_message').text('Successfully created').show()
                // clear error messages
                $('span.form-message').hide()
                setTimeout(function(){
                    window.location.reload()
                    },
                     1000)
            }
            else {
                errs = response.details
                $('#create_form_error_message').html(errs)
//                console.log(errs);
            }
        })
}


function defineNewUrl(url, key){
}


$(document).on('click', '[id^="sort-by"]', function(){
    entity = $(this).attr('name')
    url = {'users': '/account',
           'logs': '/account/users_log_data',
           'acc': '/root'
           }[entity]
    key = $(this).prop('id').replace('sort-by-', '')
    url = defineNewUrl(url, key)
    window.location.href = url;
})


function ChangePassword(){
    $('input[id^="id"]').each(function(){if ($(this).val()=='') {valid=false;} else{valid=true;}})
    if (valid){
        url = $('form#password_change_form').attr('action')
        $.post(url, $('form#password_change_form').serialize(), function(response){
            response = JSON.parse(response)
            if (response.result == true){
                    $('#success_message').css('color', 'green').text('Successfully changed!').show()
                    // clear error messages
                    $('span.form-message').hide()
                    setTimeout(function(){
                        window.location.reload()
                        },
                         1000)
                }
                else {
                    console.log(response.errors);
                    $('span.form-message').css('color', 'red').text('Error!')
                }
        })
        } else {
        $('#success_message').text('Fill out all fields!').css('color', 'red')
            .slideUp(500).delay(2000).fadeOut(500)
        }
}
