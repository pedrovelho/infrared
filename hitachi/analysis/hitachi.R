print(getwd())
aircode <- read.table('/ddrive/infrared/hitachi/data/hitachi.data', header = TRUE, sep='', colClasses=rep(c('character'), times=17))

aircode$temp <- sapply(aircode$temp, as.numeric)
aircode$nbits <- sapply(aircode$nbits, as.numeric)
aircode$nbytes <- sapply(aircode$nbytes, as.numeric)

# convert hexadecimal in decimal
hex2dec <- function(x){
  decimal <- 0
  power <- 1
  result <- 0
  hexaVector <- rev(strsplit(x, "")[[1]])
  for( i in hexaVector){
    num <- 0
    if(i == 'A'){
      decimal <- 10
    }else if(i == 'B'){
      decimal <- 11
    }else if(i == 'C'){
      decimal <- 12
    }else if(i == 'D'){
      decimal <- 13
    }else if(i == 'E'){
      decimal <- 14
    }else if(i == 'F'){
      decimal <- 15
    }else{
      decimal <- as.numeric(i)
    }
    result <- result + (power * decimal)
    power <- power*16
  }
  return (result)
}
hex2dec("20")
hex2dec("0A")
hex2dec("FF")
hex2dec("01")
hex2dec("10")

# convert binary in hexadecimal 
bin2hex <- function(x){
  hexCode <- ''
  for( i in seq(1, nchar(x), 4) ){
    bits <- substring(x, i, i+3)
    bits <- strsplit(bits, "")[[1]]
    num <- 0
    num <- 8*as.numeric(bits[1])
    num <- num + 4*as.numeric(bits[2])
    num <- num + 2*as.numeric(bits[3])
    num <- num + as.numeric(bits[4])
    if(num == 10){
      digit <- 'A'
    }else if(num == 11){
      digit <- 'B'      
    }else if(num == 12){
      digit <- 'C'      
    }else if(num == 13){
      digit <- 'D'      
    }else if(num == 14){
      digit <- 'E'      
    }else if(num == 15){
      digit <- 'F'      
    }else {
      digit <- as.character(num)
    }
    hexCode = paste(hexCode, digit, sep="")
  }
  return (hexCode)
}
bin2hex("11110010")
bin2hex("1010")
bin2hex("10100110")
bin2hex("11000111")
bin2hex("10110111")
bin2hex("11100111")

# convert binary in decimal
bin2dec <- function(x){
  sum <- 0
  power2 <- 1
  for( i in rev(strsplit(x, "")[[1]]) ){
    sum <- sum + as.numeric(i)*power2
    power2 <- power2*2
  }
  return (sum)
}
bin2dec("11110010")
bin2dec("1010")
bin2dec("10100110")
bin2dec("11000111")
bin2dec("10110111")
bin2dec("11100111")
bin2dec("11111111")

# create column that split the bitstring into bytes LSB first order
aircode$decoded_bin <- lapply(aircode$bitstring, function(x){
  bits <- strsplit(x, "")[[1]]
  bCount <- 0
  byteStr <- ''
  decodedStr <- c()
  for (b in bits){
    bCount <- bCount + 1
    # LSB first order, big endian
    byteStr <- paste(b, byteStr, sep='')
    if(bCount == 8){
      bCount <- 0
      decodedStr <- c( decodedStr , byteStr )
      byteStr <- ''
    }
  }
  return (decodedStr)
})

# convert the decoded_bin column into hexa, create a new decoded_hexa column
aircode$decoded_hex <- lapply(aircode$decoded_bin, function(x){
  decodedHex <- c()
  for (i in x){
    decodedHex <- c(decodedHex, bin2hex(i))
  }
  return (decodedHex)
})

# convert the decoded_dec column into decimal, create a new decoded_dec column
aircode$decoded_dec <- lapply(aircode$decoded_bin, function(x){
  decodedHex <- c()
  for (i in x){
    decodedHex <- c(decodedHex, bin2dec(i))
  }
  return (decodedHex)
})

# Create a table in HEXADECIMAL with bytes as rows and samples as columns
# complete with NA's if the signal has less then 44 bytes
hexa <- data.frame(sapply(aircode$decoded_hex, function(x){
  x <- c(x, rep('NA', 44 - length(x) ))
  return (x)
}))

# Create a table in BINARY with bytes as rows and samples as columns
# complete with NA's if the signal has less then 44 bytes
bita <- data.frame(sapply(aircode$decoded_bin, function(x){
  x <- c(x, rep('NA', 44 - length(x) ))
  return (x)
}))

# Create a table in DECIMAL with bytes as rows and samples as columns
# complete with NA's if the signal has less then 44 bytes
deca <- data.frame(sapply(aircode$decoded_dec, function(x){
  x <- c(x, rep('NA', 44 - length(x) ))
  return (x)
}))

# Find fixed bytes, bytes that does not change within all samples
which(apply(hexa, 1, function(x){
  if(length(unique(x)) == 1)
    return (TRUE)
  else
    return (FALSE)
}))


# Find bytes that are always the same value ignoring LAST SAMPLE, the INFO 
# command has a short sequence of only 21 bytes
filteredColumns <- seq(1,length(hexa[1,])-1)
bytesThatChange <- which(apply(hexa[,filteredColumns], 1, function(x){
  if(length(unique(x)) == 1)
    return (FALSE)
  else
    return (TRUE)
}))

# Create data.frames filtering columns that never change
hexaFiltered <- hexa[bytesThatChange,]
decaFiltered <- deca[bytesThatChange,]
bitaFiltered <- bita[bytesThatChange,]

# Loop on all decimal samples, used to figure out the parity algorithm
for(i in names(deca[,1:37])){
  fixedBytes = c(1,2,3,4,5,6,7,9,13,17,19,20,21,22,23,24,25)
  vect = as.numeric(as.character(deca[fixedBytes,i]))
  fixe <- sum(vect) %% 256
  # knwon positive bytes that will decrease parity if increased
  knownPositive <- c(18)
  posi <- sum(as.numeric(as.character(deca[knownPositive,i]))) %% 256
  # knwon negative bytes that will decrease parity if increased
  knownNegative <- c(8,10,11,12,14,15,16,26,27)
  nega <- sum(as.numeric(as.character(deca[knownNegative,i]))) %% 256
  target <- as.numeric(as.character(deca[28,i]))
  print(c(i,":", posi, nega, target, posi+108 -nega, fixe), sep=" ")
}

# Modular add of 2 binary string of bytes must have the same size
addByte <- function(x, y){
  x <- strsplit(x, "")[[1]]
  y <- strsplit(y, "")[[1]]
  r <- rep('0', length(x))
  carryBit <- '0'
  for (i in seq(length(x), 1, -1)){
    if(x[i] != y[i]){
      if(carryBit == '1'){
        r[i] <- '0'
        carryBit <- '1'
      }else{
        r[i] <- '1'
      }
    }else if(x[i] == '1' && y[i] == '1'){
      if(carryBit == '1'){
        r[i] <- '1'
      }else{
        r[i] <- '0'
      }
      carryBit <- '1'
    }else{
      if(carryBit == '1'){
        r[i] <- '1'
      }else{
        r[i] <- '0'
      }
      carryBit <- '0'
    }
  }
  return (paste(r, collapse=''))
}
addByte('001', '010')
addByte('011', '001')

# Generate 2's complement of a binary string
complement2 <- function(x){
  firstOne <- FALSE
  bitString <- strsplit(x, '')[[1]]
  result2 <- rep('0', length(bitString))
  for (i in seq(length(bitString), 1, -1)){
    if(firstOne){
      if(bitString[i] == '1'){
        result2[i] <- '0'
      }else{
        result2[i] <- '1'
      }
    }else{
      if(bitString[i] == '1'){
        result2[i] <- '1'
      }else{
        result2[i] <- '0'
      }
    }
    if(bitString[i] == '1'){
      firstOne <- TRUE
    }
  }
  return(paste(result2, collapse=''))
}
complement2('11110')
complement2('100101')
complement2('100000')
complement2("00010010")
complement2("00000011")
addByte(complement2("00010010"),complement2("00000011"))


# Bytes modular sum of complement 2' + complement 2' of 62 (mysterious)
checkSum <- function(x){
  sum <- rep('0', length(strsplit(x, '')[[1]]))
  sum <- paste(sum, collapse='')
  for (i in x){
    sum <- addByte(complement2(i), sum)
  }
  return (addByte(sum, complement2('11000010')))
}
checkSum(c("00010010", "00000011"))

# Check parity of 37 first samples, considering only the first sequence, 
# bytes 1-28
for(i in names(bita[,1:49])){
  nega <- checkSum(as.character(bita[1:27,i]))
  target <- as.character(bita[28,i])
  print(c(i,":", nega, bin2dec(nega), target, bin2dec(target), bin2dec(target)-bin2dec(nega)), sep=" ")
}

# Check parity of samples 1-6 and 36, considering only the second sequence
# bytes 29-44
for(i in names(bita[,c(1:7,37:48)])){
  nega <- checkSum(as.character(bita[29:43,i]))
  target <- as.character(bita[44,i])
  print(c(i,":", nega, bin2dec(nega), target, bin2dec(target), bin2dec(target)-bin2dec(nega)), sep=" ")
}

# Check parity of sample 50, info button with only 21 bytes
# bytes 1-22
nega <- checkSum(as.character(bita[1:20,50]))
target <- as.character(bita[21,50])
print(c(38,":", nega, bin2dec(nega), target, bin2dec(target), bin2dec(target)-bin2dec(nega)), sep=" ")

# All samples match !!!!!!!!!
# TODO samples with:
# sleep
# leavehome
# clean
# time programming
