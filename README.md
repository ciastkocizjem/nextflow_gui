# nextflow_gui
Projekt z Zaawansowanej Inżynierii Oprogramownaia

### Skrypt run.sh
Robi migrację bazy danych, uruchamia serwer rabbitMQ i celery
- dodanie pozwolenia na wykonanie - chmod +x run.sh
- wywołanie - bash run.sh

### Testowe pipeline
- my-pipeline.nf - Hello world
- failing-process.nf - Pipeline, który zakończy się błędem
- ignore-failing-process.nf - Pipeline z błędme wykonania, który zakończy się prawidłowo
- feedback-loop-workflow.nf - Pipeline, który używa pliku wejściowej hello.txt
- process-get-workdir.nf - Zwraca nazwę folderu wykonania
- publish-rename-outputs.nf - Tworzy pliki outputowe
- task-batching.nf - Odpala kilka procesów