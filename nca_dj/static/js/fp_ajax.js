////// buttons //////
$(window).on('load', function (){
    // searchButton.click();
});
var searchButton = document.getElementById("search_button");
    if (blockButton !== null) {
        searchButton.addEventListener("click", searchTable);
    }

var blockButton = document.getElementById("block_button");
    if (blockButton !== null) {
        blockButton.addEventListener("click", blockPrac);
    }

function setSblockButtonBehaviour(buttonId) {
  var sblockButton = document.getElementById(buttonId);
  sblockButton.addEventListener("click", function(){
    sblockPrac(buttonId); // MUST use anon function in order to pass parameters to listener function !!!
  });
  console.log(buttonId + ' is listening for sblock.');
}
function setSblockButtonClassBehaviour(className) {
  var buttons = document.getElementsByClassName(className);
  for (n = 0; buttons[n]; n++) {
      button = buttons[n];
      setSblockButtonBehaviour(button.id);
  }
}

function setNoteButtonBehaviour(buttonId) {
    var noteButton = document.getElementById(buttonId);
    noteButton.addEventListener("click", function(){
        editNote(buttonId); // MUST use anon function in order to pass parameters to listener function !!!
    });
}
function setNoteButtonClassBehaviour(className) {
    var buttons = document.getElementsByClassName(className);
    for (n = 0; buttons[n]; n++) {
        button = buttons[n];
        setNoteButtonBehaviour(button.id);
    }
}

////// forms + actions //////
var searchForm = document.getElementById("search_form");
var action = searchForm.getAttribute("action");
var blockForm = document.getElementById("block_form");
    if (blockForm !== null) {
        var azione = blockForm.getAttribute("action");
    }
////// table textareas title //////
var tBody = document.getElementById("fp_table_body");
var headerRow = document.getElementById("table_header_row");
var textAreas = document.getElementsByTagName('textarea');
var h2title = document.getElementById("h2title");
var staticTitleName = h2title.innerHTML;

////// AJAX functions //////
function gatherSearchData() {
  var wheres = new FormData(searchForm); //this needs to be inside the function so that each time it's called it reads the value of searchForm items
  var whereString = 'where={';
  for ([name, value] of wheres.entries()) {
      whereString += ('"' + name + '":"' + value + '",');
  }
  var whereString = whereString.replace(/.$/,"}");

  var dataArray = [];
  for(i=0; i < textAreas.length; i++) {
    var nameValue = textAreas[i].name + '=' + textAreas[i].value;
    dataArray.push(nameValue);
  }
  dataArray.push(whereString);
  return dataArray.join('&');
}

function searchTable() {
  showSpinner();
  var xhr = new XMLHttpRequest();
  xhr.open('POST', action, true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');   // ONLY when not pure FormData
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.onreadystatechange = function () {
      if ( xhr.readyState == 4 && xhr.status == 200 ) {
        //   alert(xhr.responseText);
        //   var json = JSON.parse(xhr.responseText);
        //   tBody.innerHTML = headerRow.outerHTML + json.table_contents;
          tBody.innerHTML = headerRow.outerHTML + xhr.responseText;
          h2title.innerHTML = staticTitleName + ': ' + (tBody.getElementsByClassName('fp_table_data_row').length);
          setInputClassBehaviour('sblock_input_class');
          setSblockButtonClassBehaviour('sblock_button_class');
          setNoteButtonClassBehaviour('edit_note_button_class');
          getExportLink(data);
          hideSpinner();
      }
  };
  var data = gatherSearchData();
  xhr.send(data);
}

function getExportLink(data) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'ajax/fp_export', true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');   // ONLY when not pure FormData
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.onreadystatechange = function () {
      if ( xhr.readyState == 4 && xhr.status == 200 ) {
          $('#export_link').attr("href", xhr.responseText);
      }
  };
  xhr.send(data);
}

function blockPrac() {
  showSpinner();
  var blockFormData = new FormData(blockForm);
  var validData = validateFormData(blockFormData);
  if (validData === false) {
      return;
  }
  var xhr = new XMLHttpRequest();
  xhr.open('POST', azione, true);
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.onreadystatechange = function () {
      if ( xhr.readyState == 4 && xhr.status == 200 ) {
          hideSpinner();
          alert(xhr.responseText);
          resetFormInputs(blockForm);
          resetFormInputs(searchForm);
          searchTable();
      }
  };
  xhr.send(blockFormData);
}

function sblockPrac(buttonId) {
  showSpinner();
  buttonId = buttonId.replace(/ /g,'');
  var stockId = buttonId.substring(buttonId.length - 7);
  var enteredDate = document.getElementById('sblock_input_'+stockId).value;
  var isDateCorrect = verifyDate(enteredDate);
  if (isDateCorrect === false) {
    return;
  }
  var day = enteredDate.slice(0, 2);
  var month = enteredDate.slice(2, 4);
  var year = enteredDate.slice(4, 8);
  var sqlDate = year+month+day;

  var data = "StockID="+stockId+"&rilasciato="+sqlDate ;

  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'ajax/sblock', true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded'); //ONLY when NOT pure FormData
  xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
  xhr.onreadystatechange = function () {
      if ( xhr.readyState == 4 && xhr.status == 200 ) {
          hideSpinner();
          alert(xhr.responseText);
          searchTable();
      }
  };
  xhr.send(data);
  // xhr.send("first_name=Bob&last_name=Smith");
}

function editNote(buttonId) {
    showSpinner();
    var stockId = buttonId.substring(buttonId.length - 7);
    var note = document.getElementById('note_input_'+stockId).value;
    var data = "StockID="+stockId+"&note="+note ;
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'ajax/sblock', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded'); //ONLY when NOT pure FormData
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onreadystatechange = function () {
      if ( xhr.readyState == 4 && xhr.status == 200 ) {
          hideSpinner();
          alert(xhr.responseText);
          searchTable();
      }
    };
    xhr.send(data);
}
