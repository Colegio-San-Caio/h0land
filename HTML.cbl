      * HTML.cbl - writes bluh_cob.html (fixed format)
       IDENTIFICATION DIVISION.
       PROGRAM-ID. HTML-GEN.
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT OUT-FILE ASSIGN TO "bluh_cob.html"
               ORGANIZATION IS LINE SEQUENTIAL.
       DATA DIVISION.
       FILE SECTION.
       FD  OUT-FILE.
       01  OUT-REC      PIC X(200).
       WORKING-STORAGE SECTION.
       COPY "BLUH.cpy".
       01  WS-LINE      PIC X(200).
       PROCEDURE DIVISION.
       MAIN-PARA.
           OPEN OUTPUT OUT-FILE
           MOVE '<!doctype html>' TO WS-LINE
           PERFORM PUT-LINE
           MOVE '<meta charset="utf-8">' TO WS-LINE
           PERFORM PUT-LINE
           MOVE '<title>BLUH :: COBOL</title>' TO WS-LINE
           PERFORM PUT-LINE
           MOVE '<style>' TO WS-LINE
           PERFORM PUT-LINE
           MOVE 'body{background:#000;margin:20px}' TO WS-LINE
           PERFORM PUT-LINE
           MOVE '.box{border:1px solid #1c2430;' TO WS-LINE
           PERFORM PUT-LINE
           MOVE 'border-radius:10px;padding:12px;' TO WS-LINE
           PERFORM PUT-LINE
           MOVE 'background:#0d1014;color:#3dff9a;' TO WS-LINE
           PERFORM PUT-LINE
           MOVE 'font:13px monospace}' TO WS-LINE
           PERFORM PUT-LINE
           MOVE '</style>' TO WS-LINE
           PERFORM PUT-LINE
           MOVE '<div class="box">' TO WS-LINE
           PERFORM PUT-LINE
           MOVE '<b>OBSIDIAN MAINFRAME :: BLUH</b>' TO WS-LINE
           PERFORM PUT-LINE
           STRING '<p>GRID ' BLUH-GRID-X 'x' BLUH-GRID-Y
               ' BLOCK ' BLUH-BLOCK-X 'x' BLUH-BLOCK-Y '</p>'
               DELIMITED BY SIZE INTO WS-LINE
           PERFORM PUT-LINE
           MOVE '<pre>[STUB] GREETINGS, OPERATOR.</pre>'
               TO WS-LINE
           PERFORM PUT-LINE
           MOVE '</div>' TO WS-LINE
           PERFORM PUT-LINE
           CLOSE OUT-FILE
           DISPLAY "WROTE bluh_cob.html"
           STOP RUN.
       PUT-LINE.
           WRITE OUT-REC FROM WS-LINE
           MOVE SPACES TO WS-LINE.
