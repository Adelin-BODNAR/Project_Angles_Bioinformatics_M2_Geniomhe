install.packages(rjson)
library(rjson)
name<-commandArgs(trailingOnly = TRUE)[3]
output_filename <- commandArgs(trailingOnly = TRUE)[2]

data_DSSR <- fromJSON(file=commandArgs(trailingOnly = TRUE)[1])



distribution<-function(data_json){
  theta<-c()
  for(rp in names(data_json)) {
  theta<-c(theta,na.omit(as.numeric(data_json[[rp]]$angles$theta)))
  }
  return(theta)
}

classes <- function(theta_data) {
  val_min <- min(theta_data)
  val_max <- max(theta_data)
  pdf(output_filename) 
    hist(theta_data, main = paste("Distribution des valeurs de theta -", name),
                   xlab = "Valeurs de theta", ylab = "Fréquence", col = "lightblue", border = "black",xlim = c(-190,190))
    legend("topright", legend = c(paste("Min: ", round(val_min, 2)), paste("Max: ", round(val_max, 2))),
         col = c("red", "red"), bty = "n", cex = 0.8)
  dev.off()
}

theta_train<-distribution(data_DSSR)


train<-classes(theta_train)


