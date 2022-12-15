#!/usr/bin/env nextflow

/*
 * Copyright (c) 2018, Centre for Genomic Regulation (CRG).
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

 /*
  * author Ben Sherman <bentshermann@gmail.com>
  */

nextflow.preview.recursion=true

params.input = "$baseDir/hello.txt"

process tick {
  input:
    path 'input.txt'
  output:
    path 'result.txt'
  script:
    """
    cat input.txt > result.txt
    echo "Task ${task.index} : tick" >> result.txt
    """
}

process tock {
  input:
    path 'input.txt'
  output:
    path 'result.txt'
  script:
    """
    cat input.txt > result.txt
    echo "Task ${task.index} : tock" >> result.txt
    """
}

workflow clock {
  take: infile
  main:
    infile | tick | tock
  emit:
    tock.out
}

workflow {
  clock
    .recurse(file(params.input))
    .until { it -> it.size() > 1000 }

  clock
    .out
    .view(it -> it.text)
}
