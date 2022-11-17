params.str = 'Hello world!'

process sleep {

  """
  this produces error
  """
}

workflow {
  sleep
}
