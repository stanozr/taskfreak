$('document').ready(function() {
    if(typeof dragula === "function"){
        // lists reorder
        var drake = dragula({
            isContainer: function (el) {
                return el.classList.contains('project-dragula');
            },
            moves: function (el, container, handle) {
                return handle.classList.contains('gu-handle');
            },
            revertOnSpill: true
        }).on('drop', function(el) {
            $l = $(el);
            $f = $l.closest('form');
            pid = $f.find("input[name='pid']").val()
            $.ajax({
                method: "POST",
                url: $f.attr('action'),
                data: $f.serialize()
            }).done(function (data) {
                if (data.error) {
                    tfk_toasted(data.error, 'text-bg-danger');
                } else {
                    tfk_toasted(data.success, 'text-bg-success');
                }
            });
        });

        $('.btn-list-delete').click(function() {
            $t = $(this);
            lid = $t.data('lid');
            ln = $t.siblings('input').val();
            // -TODO- check if list is empty
            tfk_confirm("Delete list <i>"+ln+"</i>?", "/api/project/lists/del/"+lid)
            // $.getJSON( "/api/project/lists/del/"+lid)
            //     .done(function( data ) {
            //         if (data.error) {
            //             tfk_toasted(data.error, 'text-bg-danger');
            //         } else {
            //             $t.closest('li').remove();
            //             tfk_toasted(data.success, 'text-bg-success');
            //         }
            //     });
        });
    }

    $('.btn-project-edit').click(function() {
        var pid = $(this).data('id');
        $.getJSON( "/api/project/load/"+pid )
            .done(function( json ) {
                var $m = $('#editModal');
                $m.find('#iId').val(json.id);
                $m.find('#iTitle').val(json.title);
                $m.find('#iDescription').val(json.description);
                $m.find('#iBudget').val(json.budget);
                $m.find('#iStart').parent().datepicker('update', json.start);
                $m.find('#iDeadline').parent().datepicker('update',json.deadline);
                $m.find('#iStatus').val(json.status);
                bootstrap.Modal.getOrCreateInstance('#editModal').show();
            })
            .fail(function( jqxhr, textStatus, error ) {
                var err = textStatus + ", " + error;
                console.log( "Request Failed: " + err );
            });
    });

    $('button[data-member-ids]').click(function(event) {
        $t = $(this);
        $("#usersModal input[name='pid']").val($t.data('project-id'));
        mids = $t.data('member-ids');
        $ug = $('#usersModal .users-grid');
        $ug.find('.btn-user').removeClass('btn-active').show();
        mids.forEach(mid =>  $ug.find('#usrsel-'+mid).hide());
    });

    $(".users-grid input[type='checkbox']").change(function() {
        $t = $(this);
        if ($t.prop( "checked" )) {
            $t.closest('.btn-user').addClass('btn-active');
        } else {
            $t.closest('.btn-user').removeClass('btn-active');
        }
    });

    $('#editModal').on('hidden.bs.modal', function() {
        $f = $(this);
        if ($f.find("input[name='id']").val()) {
            $f.find("form.modal-content")[0].reset();
        }
    });
    
    $('#project-form, form.card-project, #usersModal form').submit(function( event ) {
        $t = $(this);
        $.ajax({
            method: "POST",
            url: $t.attr('action'),
            data: $t.serialize()
        }).done(function (data) {
            if (data.error) {
                tfk_toasted(data.error, 'text-bg-danger');
            } else if (data.noreload) {
                tfk_toasted(data.success, 'text-bg-success');
            } else {
                // -TODO- better target modals (and review form/node selector as well)
                bootstrap.Modal.getOrCreateInstance('#editModal').hide();
                bootstrap.Modal.getOrCreateInstance('#usersModal').hide();
                location.reload();
            }
        });
        event.preventDefault();
    });
});

