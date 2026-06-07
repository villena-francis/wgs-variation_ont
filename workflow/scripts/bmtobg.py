import gzip
import sys

sys.stdout = open(snakemake.log.o, "w")
sys.stderr = open(snakemake.log.e, "w")

fname = snakemake.input["bedmethyl"]

ofh = {
    "m": {
        "fw": open(snakemake.output["mfw"], "w"),
        "rv": open(snakemake.output["mrv"], "w"),
    },
    "h": {
        "fw": open(snakemake.output["hfw"], "w"),
        "rv": open(snakemake.output["hrv"], "w"),
    },
}

with gzip.open(fname) as ifh:
    for l in ifh:
        values = l.decode().split()
        ch = values[0]
        start = values[1]
        end = values[2]
        mod = values[3]
        strand = "fw" if values[5] == "+" else "rv"
        pct = values[10]
        ofh[mod][strand].write("\t".join([ch,start,end,pct]) + "\n")

for mod in ofh:
    for strand in ofh[mod]:
        ofh[mod][strand].close()
