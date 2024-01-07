import os

class AngleHelper:
  def __init__(self, *args, **kwargs):
    # TO BE COMPLETE
    pass


  def predict(self, in_path: str, out_path: str):
    """
    Function that should predict the angles for the sequence of nucleotides
    Args:
      - in_path: path to a `fasta` file.
        Example:
          "
          >17EP
          ACGUUCU
          "
      - out_path: path to a `.json` file where will be stored the prediciton.
        It should have the following keys: (example with `alpha` angle)
          {
            "17EP": {
              "sequence": "ACGUUCU",
              "angles": {"alpha": [0, 0, 0, 0, 0, 0, 0]}
            }

          }
    """
    return None

if __name__ == "__main__":
    # Example of usage
    in_path = os.path.join("data", "sample", "example.fasta")
    out_path = "sample.json"
    angle_helper = AngleHelper()
    angle_helper.predict(in_path, out_path)