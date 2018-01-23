properties([
    buildDiscarder(logRotator(numToKeepStr: '20', artifactNumToKeepStr: '20')),
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
            checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'LocalBranch', localBranch: '**']], submoduleCfg: [], userRemoteConfigs: [[credentialsId: 'feygin.lena@gmail.com', url: 'git@github.com:lenks01/taboola.git']]])
        }
        stage ('build') {
            // withEnv(["JAVA_HOME=${ tool name: 'jdk-8u162', type: 'jdk' }", "PATH+MAVEN=${tool name: 'maven-3.5.2', type: 'maven'}/bin:${env.JAVA_HOME}/bin"]) {
                sh "mvn -f calc/pom.xml --batch-mode -V -U -e clean install -Dsurefire.useFile=false"
            // }
        }
        stage ('prepare release') {
            // withEnv(["JAVA_HOME=${ tool name: 'jdk-8u162', type: 'jdk' }", "PATH+MAVEN=${tool name: 'maven-3.5.2', type: 'maven'}/bin:${env.JAVA_HOME}/bin"]) {
                // sh "git config user.email 'feygin.lena@gmail.com'"
                // sh "git config user.name 'Lena Feygin'"
                sh "mvn -f calc/pom.xml --batch-mode -V -U -e release:clean release:prepare"
            // }
        }
        stage ('create RPM') {
            sh "mvn -f calc/pom.xml --batch-mode -V e rpm:attached-rpm"
        }
    }
}