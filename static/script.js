var weekpicker, week = {},
  isoMonday, daysOfWeek = {
    "monday": 1,
    "tuesday": 2,
    "wednesday": 3,
    "thursday": 4,
    "friday": 5
  };

// Load data from server to schedule table
function refreshScheduleTable(isoWeek) {
  $.ajax({
    url: "/api/v1/schedule/" + isoWeek,
    type: "GET",
    dataType: "json",
    success: function(schedule) {
      $('#scheduleTable').bootstrapTable('load', schedule);
    }
  });
}

// Load data from server to employees table
function refreshEmployeesTable() {
  $.ajax({
    url: '/api/v1/employees',
    type: 'GET',
    dataType: "json",
    success: function(employees) {
      $('#employeesTable').bootstrapTable('load', employees);
    }
  });
}

// Return date in ISO week format (2017-W32)
function getISOWeek() {
  return isoMonday.isoWeekYear() + "-W" + isoMonday.isoWeek();
}

// Return date in ISO week format (2017-W32-2)
function getISOWeekDay(dayOfWeek) {
  return getISOWeek() + "-" + daysOfWeek[dayOfWeek];
}

// Return string in ISO or dd.mm format
function formatDateToString(date, format) {
  // 01, 02, 03, ... 29, 30, 31
  var dd = (date.getDate() < 10 ? '0' : '') + date.getDate();
  // 01, 02, 03, ... 10, 11, 12
  var MM = ((date.getMonth() + 1) < 10 ? '0' : '') + (date.getMonth() + 1);
  // 1970, 1971, ... 2015, 2016, ...
  var yyyy = date.getFullYear();

  // Return date in format
  if (format == 'isoWeek') {
    return moment(date).isoWeekYear() + "-W" + isoMonday.isoWeek();
  } else if (format == 'iso') {
    return (yyyy + "-" + MM + "-" + dd);
  } else if (format == 'dd.mm') {
    return (dd + '.' + MM);
  } else {
    return 'undefind';
  }
}

function setWeekPicker(date) {
  isoMonday = moment(new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 1));

  // Create field with dates in schedule object
  for (var i = 0; i < 5; i++) {
    var day = daysOfWeek[i];
    var dateObj = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + (i + 1));
    week[day] = getISOWeekDay(day);
    var content = formatDateToString(dateObj, 'dd.mm');
    $('#scheduleTable tr:nth-child(2)>th:nth-child(' + (i + 2) + ')').html(content);
  }

  refreshScheduleTable(getISOWeek());

  weekpicker.datepicker('update', new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 1));
  // weekpicker.val(arcDay1.getFullYear() + '-' + months[arcDay1.getMonth()] + '-' + arcDay1.getDate() + ', ' + arcDay1.getFullYear() + '-' + months[arcDay1.getMonth()] + '-' + arcDay1.getDate());
}

$(function() {

  // Set weekpicker
  weekpicker = $('#weekpicker');
  weekpicker.datepicker({
    autoclose: true,
    language: "ru",
    maxViewMode: 0,
    daysOfWeekDisabled: "0,6",
    todayBtn: "linked"
  }).on("changeDate", function(e) {
    setWeekPicker(e.date);
  });
  setWeekPicker(new Date);

  // Set refresh button depending on screen width
  if (window.innerWidth < 767) {
    $('#refreshScheduleButton').html('<span class="glyphicon glyphicon-refresh"></span>');
    $('#refreshScheduleButton').addClass('btn-sm');
  } else {
    $('#refreshScheduleButton').html('<span class="glyphicon glyphicon-refresh"></span> Обновить');
  };

  // Set onClick function to refresh button
  $('#refreshScheduleButton').click(function() {
    $('#scheduleTable').bootstrapTable('refresh');
  });

  // Set login modal
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
            success: function() {
              $('#loginModal').modal('toggle');
              $('#manageModal').modal('show');
            },
            error: function() {
              $.notify("Неверный пароль", {
                type: "danger"
              });
              $('#passwordGroup').addClass('has-error');
            }
          });
        }
      });
    })
    .on('hidden.bs.modal', function(e) {
      $('#inputPassword').val('');
      $('#loginForm').validator('destroy');
    })

  // Set settings for bootstrap editable
  $.fn.editable.defaults.source = [{
      value: 'X',
      text: 'X'
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
  $.fn.editable.defaults.url = '/api/v1/schedule';
  $.fn.editable.defaults.ajaxOptions = {
    type: "PUT"
  };
  $.fn.editable.defaults.emptytext = 'X';
  $.fn.editable.defaults.display = function(value) {
    $(this).text(value);
  };
  $.fn.editable.defaults.params = function(params) {
    var data = {};
    dayOfWeek = params.name; // moday, tuesday, ... , friday
    data['shortname'] = params.pk;
    data['iso_week'] = getISOWeekDay(dayOfWeek);
    data['shift'] = params.value;
    return data;
  };
  $.fn.editable.defaults.success = function(response, newValue) {
    $.notify("Расписание обновлено", {
      type: "success"
    });
  };
  $.fn.editable.defaults.error = function(response, newValue) {
    $.notify("При обновлении расписания возникли ошибки", {
      type: "danger"
    });
  };

  // Set up default settings for notifications
  $.notifyDefaults({
    allow_dismiss: false,
    z_index: 10031,
    placement: {
      from: "bottom",
      align: "right"
    },
    delay: 1
  });

  // Set manage modal
  $('#manageModal')
    .on('shown.bs.modal', function(e) {
      refreshEmployeesTable();
    });

  // Set modal for adding employees
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
            url: '/api/v1/employees',
            type: 'POST',
            data: $('#addEmployeeForm').serialize(),
            statusCode: {
              201: function() {
                $.notify("Пользователь добавлен", {
                  type: "success"
                });
                $('#addEmployeeModal').modal('toggle');
                refreshEmployeesTable();
                refreshScheduleTable(getISOWeek());
              },
              400: function() {
                $.notify("Неверные имя или фамилия", {
                  type: "danger"
                });
                $('#nameGroup').addClass('has-error');
                $('#surnameGroup').addClass('has-error');
              }
            },
            error: function() {
              $.notify("При добавлении пользователя позникла ошибка", {
                type: "danger"
              });
              $('#nameGroup').addClass('has-error');
              $('#surnameGroup').addClass('has-error');
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

  // Set onClick function to button for delete employees
  $('#deleteEmployeeButton').click(function() {
    $.ajax({
      url: '/api/v1/employees',
      type: 'DELETE',
      data: {
        name_rus: $('#employeesTable').bootstrapTable('getSelections')[0]['name_rus'],
        surname_rus: $('#employeesTable').bootstrapTable('getSelections')[0]['surname_rus']
      },
      statusCode: {
        200: function() {
          $.notify("Пользователь удалён", {
            type: "success"
          });
          refreshEmployeesTable();
          refreshScheduleTable(getISOWeek());
        }
      },
      error: function() {
        $.notify("При удалении пользователя позникла ошибка", {
          type: "danger"
        });
      }
    });
  })

});
