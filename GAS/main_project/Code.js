var SPREADSHEET_ID = "1BKTNLVsSE2kuSEyRpEVRL2t-vkeqZEJyyXHBhCl5F1Q";

function doGet(e) {
  var unit = (e && e.parameter && e.parameter.unit) || "m1_01";
  return HtmlService.createTemplateFromFile('Index_' + unit)
      .evaluate()
      .setTitle('사라진 아틀란티스 (' + unit + ')')
      .addMetaTag('viewport', 'width=device-width, initial-scale=1')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function recordStart(studentId, name, unit) {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  
  // 시트 이름 결정
  var sheetName = unit ? ("기록_" + unit) : "기록";
  var sheet = ss.getSheetByName(sheetName);
  
  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
  }
  
  // 헤더가 비어있다면 생성 (완료 열 추가)
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(["학번", "이름", "시작 시간", "종료 시간", "소요 시간", "완료"]);
  }
  
  var startTime = new Date();
  var formattedTime = Utilities.formatDate(startTime, "Asia/Seoul", "yyyy-MM-dd HH:mm:ss");
  
  // 신규 행 작성
  sheet.appendRow([studentId, name, formattedTime, "", "", ""]);
  var rowNum = sheet.getLastRow();
  
  // 6열에 체크박스 삽입하고 미완료(체크 해제) 상태 및 빨간색 배경 지정
  var checkboxRange = sheet.getRange(rowNum, 6);
  checkboxRange.insertCheckboxes();
  checkboxRange.setValue(false);
  checkboxRange.setBackground("#FFD2D2"); // 연한 빨강
  
  // 작성된 데이터의 행 번호를 프론트엔드로 리턴
  return rowNum;
}

function recordEnd(rowNum, unit) {
  if (!rowNum) return;
  
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  
  // 시트 이름 결정
  var sheetName = unit ? ("기록_" + unit) : "기록";
  var sheet = ss.getSheetByName(sheetName);
  if (!sheet) return;
  
  var endTime = new Date();
  var formattedEndTime = Utilities.formatDate(endTime, "Asia/Seoul", "yyyy-MM-dd HH:mm:ss");
  
  // 시작 시간을 가져와서 차이를 계산
  var startVal = sheet.getRange(rowNum, 3).getValue();
  var elapsedStr = "";
  
  if (startVal) {
    var startTime = new Date(startVal);
    var elapsedMs = endTime.getTime() - startTime.getTime();
    var minutes = Math.floor(elapsedMs / 60000);
    var seconds = Math.floor((elapsedMs % 60000) / 1000);
    elapsedStr = minutes + "분 " + seconds + "초";
  }
  
  // 4열(종료 시간) 및 5열(소요 시간) 업데이트
  sheet.getRange(rowNum, 4).setValue(formattedEndTime);
  sheet.getRange(rowNum, 5).setValue(elapsedStr);
  
  // 6열의 체크박스를 완료(체크 설정) 상태 및 초록색 배경으로 업데이트
  var checkboxRange = sheet.getRange(rowNum, 6);
  checkboxRange.setValue(true);
  checkboxRange.setBackground("#D1FAE5"); // 연한 초록
  
  return true;
}

function initSheets() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var units = ["m1_01", "m1_02", "m1_03", "m1_04", "m1_05", "m1_06", "m1_07", "m1_08"];
  
  for (var i = 0; i < units.length; i++) {
    var sheetName = "기록_" + units[i];
    var sheet = ss.getSheetByName(sheetName);
    if (!sheet) {
      sheet = ss.insertSheet(sheetName);
    }
    // 헤더가 비어있다면 생성
    if (sheet.getLastRow() === 0) {
      sheet.appendRow(["학번", "이름", "시작 시간", "종료 시간", "소요 시간", "완료"]);
    }
  }
}
