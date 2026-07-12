function doGet() {
  return HtmlService.createTemplateFromFile('Index')
      .evaluate()
      .setTitle('사라진 아틀란티스 (중1 4단원)')
      .addMetaTag('viewport', 'width=device-width, initial-scale=1')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function recordStart(studentId, name) {
  var sheetId = "1BKTNLVsSE2kuSEyRpEVRL2t-vkeqZEJyyXHBhCl5F1Q";
  var ss = SpreadsheetApp.openById(sheetId);
  var sheet = ss.getSheetByName("기록");
  
  if (!sheet) {
    sheet = ss.insertSheet("기록");
  }
  
  // 만약 헤더(첫 줄)가 비어있다면 초기 설정
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(["학번", "이름", "시작 시간", "종료 시간", "소요 시간"]);
  }
  
  var startTime = new Date();
  var formattedTime = Utilities.formatDate(startTime, "Asia/Seoul", "yyyy-MM-dd HH:mm:ss");
  
  // 신규 행 작성
  sheet.appendRow([studentId, name, formattedTime, "", ""]);
  
  // 작성된 데이터의 행 번호를 프론트엔드로 리턴
  return sheet.getLastRow();
}

function recordEnd(rowNum) {
  if (!rowNum) return;
  
  var sheetId = "1BKTNLVsSE2kuSEyRpEVRL2t-vkeqZEJyyXHBhCl5F1Q";
  var ss = SpreadsheetApp.openById(sheetId);
  var sheet = ss.getSheetByName("기록");
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
  
  return true;
}
