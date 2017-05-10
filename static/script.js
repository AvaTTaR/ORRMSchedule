$(function() {
  // Schedule tabs
  $('#myTab a:first').tab('show');
  $('.navbar-btn').tab('show');

  // Check screen
  if (window.innerWidth < 768) {
    $('#refreshThisWeekButton').html('<i class="glyphicon glyphicon-refresh"></i>');
    $('#refreshThisWeekButton').addClass('btn-sm');
    $('#refreshNextWeekButton').html('<i class="glyphicon glyphicon-refresh"></i>');
    $('#refreshNextWeekButton').addClass('btn-sm');
  } else {
    $('#refreshThisWeekButton').html('<i class="glyphicon glyphicon-refresh">Обновить</i>');
    $('#refreshNextWeekButton').html('<i class="glyphicon glyphicon-refresh">Обновить</i>');
  };

  // Login Modal
  $('#loginModal')
    .on('shown.bs.modal', function(e) {
      $("#inputPassword").focus();
      $('#loginForm').validator().on('submit', function(e) {
        var password = $('#inputPassword').val();
        if (e.isDefaultPrevented()) {
          $('alert').alert();
        } else {
          e.preventDefault();
          $.ajax({
            url: '/',
            type: 'POST',
            data: $('#loginForm').serialize(),
            success: function(result) {
              if (result.status == 'OK') {
                $('#loginModal').modal('toggle');
                $('#manageModal').modal('show');
              } else {
                $('#defaultAlert').alert();
                $('#passwordGroup').addClass('has-error');
              };
            }
          });
        }
      });
    })
    .on('hidden.bs.modal', function(e) {
      $('#inputPassword').val('');
      $('#loginForm').validator('destroy');
    })

  // Default settings for bootstrap editable
  $.fn.editable.defaults.source = [{
      value: ' ',
      text: ' '
    },
    {
      value: '0',
      text: '0'
    },
    {
      value: '1',
      text: '1'
    },
    {
      value: '2',
      text: '2'
    },
    {
      value: '3',
      text: '3'
    },
    {
      value: 'B',
      text: 'B'
    },
    {
      value: '1/2',
      text: '1/2'
    },
    {
      value: '2/B',
      text: '2/B'
    },
    {
      value: '3/B',
      text: '3/B'
    }
  ]
  $.fn.editable.defaults.mode = 'inline';
  $.fn.editable.defaults.type = 'select';
  $.fn.editable.defaults.showbuttons = false;
  $.fn.editable.defaults.pk = 'shortname';
  $.fn.editable.defaults.url = '/schedule';
  $.fn.editable.defaults.emptytext = 'X';
  $.fn.editable.defaults.params = function (params) {
    var data = {};
    data['shortname'] = params.pk;
    data['date'] = params.name;
    data['shift'] = params.value;
    return data;
  };
  $.fn.editable.defaults.success = function(response, newValue) {
    if (response.status == 'OK') {
      $.notify("Расписание обновлено", {type: "success"});
    } else {
      $.notify("При обновлении расписания возникли ошибки", {type: "danger"});
    };
  };

  //Bootstrap notify default settings
  $.notifyDefaults({
    allow_dismiss: false,
    z_index: 10031,
    placement: {
      from: "bottom",
      align: "right"
    },
    delay: 1
  });

  //Refresh buttons
  $('#refreshThisWeekButton').click(function() {
    $('#thisWeekTable').bootstrapTable('refresh')
  });
  $('#refreshNextWeekButton').click(function() {
    $('#nextWeekTable').bootstrapTable('refresh')
  });

  // Employee modal
  $('#addEmployeeModal')
    .on('shown.bs.modal', function(e) {
      $("#inputName").focus();
      $('#addEmployeeForm').validator().on('submit', function(e) {
        var name_rus = $('#inputName').val();
        var surname_rus = $('#inputSurname').val();
        if (e.isDefaultPrevented()) {
          $('alert').alert();
        } else {
          e.preventDefault();
          $.ajax({
            url: '/add_employee',
            type: 'POST',
            data: $('#addEmployeeForm').serialize(),
            success: function(result) {
              if (result.status == 'OK') {
                $.notify("Пользователь добавлен", {type: "success"});
                $('#addEmployeeModal').modal('toggle');
                $('#employeeTable').bootstrapTable('refresh');
                $('#thisWeekTable').bootstrapTable('refresh');
              } else {
                $.notify("При добавлении пользователя позникла ошибка", {type: "danger"});
                $('#nameGroup').addClass('has-error');
                $('#surnameGroup').addClass('has-error');
              };
            }
          });
        }
      });
    })
    .on('hidden.bs.modal', function(e) {
      $('#inputName').val('');
      $('#inputSurname').val('');
      $('#loginForm').validator('destroy');
      $('#defaultAlert').alert();
    })

  // Delete employee button
  $('#deleteEmployeeButton').click(function() {
    $.ajax({
      url: '/delete_employee',
      type: 'POST',
      data: {
        name_rus: $('#employeeTable').bootstrapTable('getSelections')[0]['name_rus'],
        surname_rus: $('#employeeTable').bootstrapTable('getSelections')[0]['surname_rus']
      },
      success: function(result) {
        if (result.status == 'OK') {
          $('#employeeTable').bootstrapTable('refresh');
          $('#thisWeekTable').bootstrapTable('refresh');
          $.notify("Пользователь удалён", {type: "success"});
        } else {
          $.notify("При удалении пользователя позникла ошибка", {type: "danger"});
        };
      }
    });
  })

});
