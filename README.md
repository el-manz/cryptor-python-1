# **CryptorPython**

## What does it do?
You can encode and decode any text consisting of ASCII symbols using Caesar, Vigenere or Vernam cipher. Also the frequency analysis for Caesar decoding is available, but note that firstly, it isn't working with any other cipher, secondly, it is just an estimate decryption of the text. You can read about: Caesar cipher (https://en.wikipedia.org/wiki/Caesar_cipher),
Vigenere cipher (https://en.wikipedia.org/wiki/Vigenère_cipher),
Vernam cipher (https://en.wikipedia.org/wiki/One-time_pad).
<img width="612" alt="Main window" src="https://user-images.githubusercontent.com/83511476/168632529-ff3a3413-25b9-4cbc-bb2f-4fa0e4c78a5a.png">

## Caesar, Vigenere and Vernam encryption
For encryption all you need is to upload a text file and enter either the shift for Caesar or the keyword for Vigener cipher (for Vernam cipher there is no key due to it being generated automatically).
<img width="612" alt="Encryption" src="https://user-images.githubusercontent.com/83511476/168632918-69762e80-362c-493d-a886-f0bdce0aeec5.png">

## Caesar, Vigenere and Vernam decryption
For decryption you need to upload an encrypted file and either enter the key or upload the file containing it. (Except for Vernam cipher there is no option of entering because it consist of more than one line).
<img width="612" alt="Decryption" src="https://user-images.githubusercontent.com/83511476/168633627-16bfd4e7-8936-4d26-85bc-88286964a200.png">

## Frequency analysis
For frequency analysis you just need to upload an encrypted file. The algorithm counts the frequency of each letter in the standard text and compares it to their frequencies in the given text. As a standard file I use a file containing the first two chapters of 'The Catcher in the Rye' by J.D. Salinger (found on https://www.uzickagimnazija.edu.rs/files/Catcher%20in%20the%20Rye.pdf), but you can use literally any big senseful text - the more similar it is to the topic of your encrypted text, the more precise the decryption will be.
<img width="612" alt="Frequency analysis" src="https://user-images.githubusercontent.com/83511476/168636810-6870e7ab-ddaa-417c-a64b-f8f064d3a57e.png">
