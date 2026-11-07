      * main.cob - BLUH offline stub in COBOL (fixed format)
       IDENTIFICATION DIVISION.
       PROGRAM-ID. BLUH-MAIN.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       COPY "BLUH.cpy".
       01  WS-UPPER     PIC X(80).
       01  WS-HELLO     PIC 9(4) VALUE 0.
       01  WS-WHO       PIC 9(4) VALUE 0.
       01  WS-STATUS    PIC 9(4) VALUE 0.
       01  WS-HELP      PIC 9(4) VALUE 0.
       PROCEDURE DIVISION.
       MAIN-PARA.
           SET BLUH-STUB TO TRUE
           DISPLAY "=== OBSIDIAN MAINFRAME :: BLUH ==="
           DISPLAY "GRID " BLUH-GRID-X "x" BLUH-GRID-Y
                   " BLOCK " BLUH-BLOCK-X "x" BLUH-BLOCK-Y
           DISPLAY "> " WITH NO ADVANCING
           ACCEPT BLUH-QUERY
           MOVE FUNCTION UPPER-CASE(BLUH-QUERY) TO WS-UPPER
           PERFORM ANSWER-PARA
           DISPLAY "[" BLUH-MODE "] " FUNCTION TRIM(BLUH-ANSWER)
           STOP RUN.
       ANSWER-PARA.
           MOVE SPACES TO BLUH-ANSWER
           INSPECT WS-UPPER TALLYING WS-HELLO FOR ALL "HELLO"
           INSPECT WS-UPPER TALLYING WS-WHO FOR ALL "WHO"
           INSPECT WS-UPPER TALLYING WS-STATUS FOR ALL "STATUS"
           INSPECT WS-UPPER TALLYING WS-HELP FOR ALL "HELP"
           EVALUATE TRUE
               WHEN WS-HELLO > 0
                   MOVE "GREETINGS, OPERATOR." TO BLUH-ANSWER
               WHEN WS-WHO > 0
                   MOVE "I AM BLUH, AN OBSIDIAN MAINFRAME."
                       TO BLUH-ANSWER
               WHEN WS-STATUS > 0
                   MOVE "ALL SYSTEMS NOMINAL." TO BLUH-ANSWER
               WHEN WS-HELP > 0
                   MOVE "TRY: HELLO, WHO, STATUS." TO BLUH-ANSWER
               WHEN OTHER
                   MOVE "NO MATCH IN TABLE. TYPE HELP."
                       TO BLUH-ANSWER
           END-EVALUATE.
