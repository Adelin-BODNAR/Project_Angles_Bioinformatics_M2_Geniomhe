library(rjson)
#library(pdftools)

output_filename <- commandArgs(trailingOnly = TRUE)[2]

data_DSSR <- fromJSON(file=commandArgs(trailingOnly = TRUE)[1])
resultats_file <-commandArgs(trailingOnly = TRUE)[3]


distribution <- function(data_json) {
  theta <- c()
  names_list <- character(length = length(data_json))  # Initialize a character vector to store names
  for (i in seq_along(data_json)) {
    rp <- names(data_json)[i]
    theta <- c(theta, na.omit(as.numeric(data_json[[rp]]$angles$theta)))
    names_list[i] <- rp
  }
  return(list(theta = theta, names_list = names_list))
}

classes <- function(theta_data, rp) {
  val_min <- min(theta_data)
  val_max <- max(theta_data)
  path <- paste0("data/output", output_filename)
  pdf(file = path)  # Specify the file path for the PDF
  
  nb_classes <- 1 + log2(length(theta_data))
  classes <- cut(theta_data, breaks = nb_classes)
  min_max_values <- tapply(theta_data, classes, function(x) c(min(x), max(x)))
  hist(theta_data, breaks = nb_classes, main = paste("Distribution des valeurs de theta -", output_filename),
       xlab = "Valeurs de theta", ylab = "Fréquence", col = "lightblue", border = "black", xlim = c(-190, 190))
  
  legend("topright", legend = c(paste("Min: ", round(val_min, 2)), paste("Max: ", round(val_max, 2))),
         col = c("red", "red"), bty = "n", cex = 0.8)
  legend("top", legend = paste("Classes:", levels(classes)), fill = "lightblue", bty = "n", cex = 0.8)
  dev.off()
  

  cat(resultats_file, "Classes:", levels(classes), "\n\n",file=resultats_file)
}

# Extracting values and names from the distribution function
result <- distribution(data_DSSR)
theta_train <- result$theta
names_list <- result$names_list

# Iterating through names to call the classes function
for (i in seq_along(names_list)) {
  train <- classes(theta_train, names_list[i])
}

# Close the resultats_file
close(resultats_file)


