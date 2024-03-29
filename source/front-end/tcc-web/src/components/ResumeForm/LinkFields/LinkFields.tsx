import {
  Grid,
  Typography,
  TextField,
  Button
} from '@mui/material';
import useNeverEmptyArray from 'hooks/useNeverEmptyArray';
import Link from 'models/Resume/Link';
import { Fragment } from 'react';

type Props = {
  links: Link[];
  setLinks?: (links: Link[]) => void;
  readonly?: boolean;
}

const LinkFields = ({ links, setLinks, readonly }: Props) => {

  useNeverEmptyArray(links, setLinks);

  function handleLinkTitleChange(val: string, index: number): void {
    if (setLinks) {
      let copy: Link[] = [...links];
      copy[index].title = val;
      setLinks(copy);
    }
  }

  function handleLinkUrlChange(val: string, index: number): void {
    if (setLinks) {
      let copy: Link[] = [...links];
      copy[index].url = val;
      setLinks(copy);
    }
  }

  function handleLinkDescriptionChange(val: string, index: number): void {
    if (setLinks) {
      let copy: Link[] = [...links];
      copy[index].description = val;
      setLinks(copy);
    }
  }

  function handleAddGraduation(): void {
    if (setLinks) {
      let copy: Link[] = [...links];
      copy.push({});
      setLinks(copy);
    }
  }

  function handleDeleteGraduation(): void {
    if (setLinks) {
      let copy: Link[] = [...links];
      copy.pop();
      setLinks(copy);
    }
  }

  return (
    <>
      <Grid item lg={12}>
        <Typography variant="h6" gutterBottom>Links</Typography>
      </Grid>

      {links.map((x, index) => {
        return (
          <Fragment key={index}>
            <Grid item lg={12}>
              <Typography variant="body1">Link {index + 1}</Typography>
            </Grid>

            <Grid item lg={6}>
              <TextField
                id="title"
                label="Title"
                variant="outlined"
                value={x.title}
                onChange={(e) => handleLinkTitleChange(e.target.value, index)}
                fullWidth
                disabled={readonly}
              />
            </Grid>

            <Grid item lg={6}>
              <TextField
                id="type"
                label="Url"
                variant="outlined"
                value={x.url}
                onChange={(e) => handleLinkUrlChange(e.target.value, index)}
                fullWidth
                disabled={readonly}
              />
            </Grid>

            <Grid item lg={12}>
              <TextField
                id="description"
                label="Description"
                variant="outlined"
                multiline
                rows={10}
                value={x.description}
                onChange={(e) => handleLinkDescriptionChange(e.target.value, index)}
                fullWidth
                disabled={readonly}
              />
            </Grid>

          </Fragment>
        )
      })}

      {!readonly &&
        <>
          <Grid container item display="flex" justifyContent="flex-end" alignItems="flex-end" lg={12}>
            <Button variant="contained" onClick={handleAddGraduation}>Add link</Button>

            {links.length > 1 &&
              <Button variant="outlined" onClick={handleDeleteGraduation} style={{ marginLeft: "2%" }}>Delete link</Button>}
          </Grid>
        </>}
    </>
  )
}

export default LinkFields;