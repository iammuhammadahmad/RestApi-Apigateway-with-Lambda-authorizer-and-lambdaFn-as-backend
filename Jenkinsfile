pipeline {
  agent {dockerfile true}
  environment {
    AWS_DEFAULT_REGION="us-west-1"
    AWS_CREDENTIALS=credentials('aws-credentials')
  }
  stages {
    stage('Install dependencies') {
      steps {
          sh 'pip3 install -r requirements.txt'

      }
    }
    stage('CDK bootstrap') {
      steps {
          sh 'cdk bootstrap'
      }
    }
    stage('CDK synth') {
      steps {
          sh 'cdk synth'
      }
    }
    stage('CDK deploy') {
      steps {
          sh 'cdk deploy --require-approval=never'
      }
    }
  }
}