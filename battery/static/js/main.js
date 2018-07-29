function open_preview_window() {
  window.open("", "Preview Window", "height=500,width=820");

  let original_action = document.editor.action;;
  let original_target = document.editor.target;;

  document.editor.action = "/entry/preview/";
  document.editor.method = "POST";
  document.editor.target = "Preview Window";
  document.editor.submit();

  document.editor.action = original_action;
  document.editor.target = original_target;
}

function toggle_archive_list(year) {
  $(`#archive-list-${year}`).toggle();
  $(`#angle-${year}`).toggleClass("fa-angle-right fa-angle-down");
}
