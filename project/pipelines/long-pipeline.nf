params.str = 'Hello world!'

process sleep {

  """
  sleep 10 
  """
}

workflow {
  sleep
}
