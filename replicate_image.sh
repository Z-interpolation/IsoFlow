for i in {1..200}
do
cp img_000.tif _img_`printf "%03d" $i`.tif
done
cp img_000.tif _img_000.tif
