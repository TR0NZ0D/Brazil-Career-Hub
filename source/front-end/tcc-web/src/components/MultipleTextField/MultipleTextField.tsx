import { Button, Grid, TextField } from '@mui/material';
import { debounce } from 'lodash';
import { Fragment, useState } from 'react';
import { generateGuid } from 'utilities/Generator';

type ComponentProps = {
  label: string;
  fields: any[];
  itemToPush: any,
  setFunction: (val: any[]) => void;

  required?: boolean;
  sm?: number,
  md?: number,
  lg?: number,
}

const MultipleTextField = ({
  label,
  fields,
  itemToPush,
  setFunction,
  sm = 12,
  md = 12,
  lg = 12,
  required = false,
}: ComponentProps) => {

  const [keys, setKeys] = useState<string[]>(() => {
    let keysArray: string[] = [];
    for (let i = 0; i <= fields.length; i++) {
      keysArray.push(generateGuid());
    }
    return keysArray;
  })

  function addItemToArray(): void {
    let arrCopy = [...fields];
    arrCopy.push(itemToPush);
    setFunction(arrCopy);
    setKeys([...keys, generateGuid()])
  }

  function popArrayItem(): void {
    if (fields.length > 1) {
      let arrCopy = [...fields];
      arrCopy.pop();
      setFunction(arrCopy);

      let newKeys: string[] = [...keys];
      newKeys.pop();
      setKeys(newKeys);
    }
  }

  const handleItemChange = debounce((element: HTMLInputElement, index: number) => {
    let items: any[] = [...fields];
    items[index] = element.value;
    setFunction(items);
  }, 50);

  return (
    <>
      {fields.map((_, index) => {
        const id: string = `label-${index}`;
        return (
          <Fragment key={keys[index]}>
            <Grid item lg={lg} md={md} sm={sm}>
              <TextField
                required={required}
                id={id}
                label={label + ` ${index + 1}`}
                fullWidth
                onChange={(e) => handleItemChange(e.target as HTMLInputElement, index)}
              />
            </Grid>
          </Fragment>
        )
      })}

      <Grid container item display="flex" justifyContent="flex-end">
        <Button
          variant="contained"
          onClick={addItemToArray}
          style={{ marginRight: "1%" }}>
          Add Address
        </Button>
        <Button variant="outlined" onClick={popArrayItem}>Remove Address</Button>
      </Grid>
    </>
  )
}

export default MultipleTextField;