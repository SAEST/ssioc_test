pipeline {
    agent any    
    environment {
        VENV_DIR = '/var/jenkins_home/workspace/ssioc_test/venv'
        // Establece la política CSP vacía para permitir que Jenkins muestre correctamente el HTML incrustado 
        JAVA_OPTS = "-Dhudson.model.DirectoryBrowserSupport.CSP=\"sandbox allow-scripts allow-same-origin; default-src 'none'; img-src 'self' data:; style-src 'self' 'unsafe-inline' data:; script-src 'self' 'unsafe-inline' 'unsafe-eval';\""
        // Establece las variables de allure
        APP_VERSION = '1.0.0'
        PLATFORM = 'Fedora Linux 41 (Server Edition)'
        BROWSER = 'Chromedriver: 131.0.6778.265'
    }
    stages {
        stage('Clean Up and Checkout ') {
            steps {
                deleteDir()
                //Clonar el repositorio Git
                git url: 'https://github.com/SAEST/ssioc_test.git', branch: 'main'
            }
        }
        stage('Install & Setup venv') {
            steps {
                sh "python3 -m venv ${VENV_DIR}"
            }
        }
        stage('Install Dependencies') {
            steps {
                // Activar el entorno virtual e instalar las dependencias
                sh """
                    . ${VENV_DIR}/bin/activate >  /dev/null 2>&1
                    pip install --no-cache-dir -r requirements.txt
                """
            }
        }
        stage('Preparar ambiente') {
            steps {
                script {
                    // Generar archivo environment.properties con variables de entorno
                    def alluredir = "reports/report"
                    sh "mkdir -p ${alluredir}"
                    def pytestdir = "reports/pytestreport"
                    sh "mkdir -p ${pytestdir}"
                    sh """
                        echo 'APP_VERSION=${env.APP_VERSION}' >> ${alluredir}/environment.properties
                        echo 'PLATFORM=${env.PLATFORM}' >> ${alluredir}/environment.properties
                        echo 'BROWSER=${env.BROWSER}' >> ${alluredir}/environment.properties
                        echo 'BUILD_URL=${env.BUILD_URL}'
                    """
                }
            }
        }
        stage('Ejecutar Test con Pytest, Selenium - POM') {
            steps {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                // pytest tests/test_public_page.py --html=reports/pytestreport/report2.html --self-contained-html --alluredir=reports/report
                // pytest_html_merger -i /var/jenkins_home/workspace/ssioc_test/reports/pytestreport -o /var/jenkins_home/workspace/ssioc_test/reports/pytestreport/report.html
                sh """
                    . ${VENV_DIR}/bin/activate > /dev/null 2>&1
                    pytest tests/test_public_page.py --html=reports/pytestreport/report.html --self-contained-html --alluredir=reports/report
               """
                }
            }
        }
    }
    post {
        always {
            script {
                // Ejecuta Allure
                allure includeProperties: false, jdk: '', reportBuildPolicy: 'ALWAYS', results: [[path: 'reports/report']]
                
                // Define las URLs de los reportes
                def allureReportUrl = "${env.BUILD_URL}allure"
                def reportpy = "${env.BUILD_URL}execution/node/3/ws/reports/pytestreport/report.html"

                env.BUILD_RESULT = currentBuild.currentResult
                // Convertir la duración a un formato legible
                def durationMillis = currentBuild.duration
                def durationSeconds = (durationMillis / 1000) as int
                def minutes = (durationSeconds / 60) as int
                def seconds = durationSeconds % 60
                env.BUILD_DURATION = "${minutes}m ${seconds}s"

                // Imprime las URLs en consola
                echo "El reporte de Allure está disponible en: ${allureReportUrl}"
                echo "El reporte de Pytest está disponible en: ${reportpy}"
                
                // Archiva los reportes de Pytest y datos adicionales
                archiveArtifacts artifacts: 'reports/pytestreport/report.html', allowEmptyArchive: true
                archiveArtifacts artifacts: 'data/bd/pres-csv/PRES_2024.csv', allowEmptyArchive: true

                sh """
                    . ${VENV_DIR}/bin/activate > /dev/null 2>&1
                    python3 utils/send_email.py ${env.BUILD_RESULT} ${env.BUILD_DURATION} ${env.SMTP_PASSWORD}
                """
            }
        }
    }
}
