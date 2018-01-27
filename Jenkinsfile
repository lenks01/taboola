properties([
    buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '5')),
])
pipeline {
    agent {
        label 'centos' 
    }
    options { timestamps() }
    tools {
        jdk 'jdk-8u162'
        maven 'maven-3.5.2'
    }
    stages {
        stage ('checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'LocalBranch', localBranch: '**']], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'feygin.lena@gmail.com', url: 'git@github.com:lenks01/taboola.git']]])
            }
        }
        stage ('build') {
            steps {
            // withEnv(["JAVA_HOME=${ tool name: 'jdk-8u162', type: 'jdk' }", "PATH+MAVEN=${tool name: 'maven-3.5.2', type: 'maven'}/bin:${env.JAVA_HOME}/bin"]) {
                sh "mvn -f calc/pom.xml --batch-mode -V -U -e clean install -Dsurefire.useFile=false"
            // }
            }
        }
        stage ('Install rpm locally') {
            steps {
                sh "sudo rm -rf /opt/calc"
                sh "sudo rpm -Uvh --force calc/target/rpm/taboola_calc/RPMS/noarch/*.rpm"
            }
        }
        stage ('Archive') {
            steps {
                archiveArtifacts artifacts: '**/*.rpm'
            }
        }
    }
}