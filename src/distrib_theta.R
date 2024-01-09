library(rjson)
#library(pdftools)
input_path <- 
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
  path<-paste0("/home/sea/Desktop/Fariza/Angle_RNA/ENV_angle_RNA/rna_angles_prediction_dssr/output_dir",output_filename)
  pdf(output_filename) 

  nb_classes <- 1 + log2(length(theta_data))
  classes <- cut(theta_data, breaks = nb_classes)
  min_max_values <- tapply(theta_data, classes, function(x) c(min(x), max(x)))
  hist(theta_data, breaks = nb_classes, main = paste("Distribution des valeurs de theta -", output_filename),
       xlab = "Valeurs de theta", ylab = "Fréquence", col = "lightblue", border = "black", xlim = c(-190, 190))
  
  legend("topright", legend = c(paste("Min: ", round(val_min, 2)), paste("Max: ", round(val_max, 2))),
         col = c("red", "red"), bty = "n", cex = 0.8)
  legend("top", legend = paste("Classes:", levels(classes)), fill = "lightblue", bty = "n", cex = 0.8)
  dev.off()
}

theta_train<-distribution(data_DSSR)


train<-classes(theta_train)


