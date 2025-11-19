@echo off
REM ============================================================
REM Upload Training Documents to Pinecone
REM ============================================================

echo.
echo ============================================================
echo   TRAINING DOCUMENT UPLOAD TO PINECONE
echo ============================================================
echo.
echo This will upload your training documents to Pinecone.
echo.
echo Documents found:
echo   - Official:      15 PDFs
echo   - Personal:      14 PDFs
echo   - Confidential:  0 PDFs
echo.
echo Estimated time: 15-20 minutes
echo.
pause

cd /d "%~dp0"
chcp 65001 >nul 2>&1
python scripts/upload_training_documents.py

echo.
echo ============================================================
echo Upload complete! Check summary above for results.
echo ============================================================
echo.
echo Next steps:
echo   1. Test retrieval: python scripts/test_retrieval.py
echo   2. Test AI classification: python scripts/test_groq.py  
echo   3. Start print agent: python virtual_printer_agent.py
echo.
pause
